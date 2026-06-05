import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";
import net from "node:net";
import fs from "node:fs";
import path from "node:path";

const LOG_PATH = path.join(
  process.env.HOME ?? "",
  ".pi/agent/logs/emacs-mcp.log"
);

function logLine(message: string) {
  const line = `[${new Date().toISOString()}] ${message}\n`;
  try {
    fs.mkdirSync(path.dirname(LOG_PATH), { recursive: true });
    fs.appendFileSync(LOG_PATH, line);
  } catch {
    // ignore
  }
}

const DEFAULT_SOCKET = path.join(
  process.env.HOME ?? "",
  ".emacs.d/emacs-mcp-server.sock"
);

const SOCKET_PATH = process.env.EMACS_MCP_SOCKET ?? DEFAULT_SOCKET;
const ENABLE_EVAL_ELISP = process.env.EMACS_MCP_ENABLE_EVAL_ELISP === "1";

const MCP_TOOLS: Array<{ name: string; description: string }> = [
  { name: "org-agenda", description: "Org agenda and TODO views" },
  { name: "org-search", description: "Org heading search" },
  { name: "org-get-node", description: "Fetch org heading or file body" },
  { name: "org-list-templates", description: "List org-capture templates" },
  { name: "org-list-tags", description: "List org tags with counts" },
  { name: "org-capture", description: "Create org entry via template" },
  { name: "org-update-node", description: "Update org heading properties/body" },
  { name: "org-refile", description: "Refile org heading" },
  { name: "org-archive", description: "Archive org heading" },
  { name: "org-clock", description: "Clock in/out org tasks" },
  { name: "org-roam-search", description: "Search org-roam nodes" },
  { name: "org-roam-get-node", description: "Get org-roam node + backlinks" },
  { name: "org-roam-capture", description: "Capture org-roam node" },
];

if (ENABLE_EVAL_ELISP) {
  MCP_TOOLS.push({ name: "eval-elisp", description: "Eval elisp in Emacs" });
}

function mcpRequest(socketPath: string, method: string, params: unknown) {
  return new Promise<any>((resolve, reject) => {
    if (!fs.existsSync(socketPath)) {
      logLine(`socket_missing path=${socketPath}`);
      reject(new Error(`Emacs MCP socket not found: ${socketPath}`));
      return;
    }

    const socket = net.createConnection(socketPath);
    let buffer = "";
    let initialized = false;
    let toolCallSent = false;

    const send = (msg: unknown) => {
      socket.write(`${JSON.stringify(msg)}\n`);
    };

    const cleanup = () => {
      socket.removeAllListeners();
      socket.end();
      socket.destroy();
    };

    socket.on("connect", () => {
      logLine(`connect socket=${socketPath} method=${method}`);
      send({
        jsonrpc: "2.0",
        id: 1,
        method: "initialize",
        params: {
          protocolVersion: "draft",
          capabilities: {},
          clientInfo: { name: "pi-emacs-mcp", version: "0.1.0" },
        },
      });
    });

    socket.on("data", (chunk) => {
      buffer += chunk.toString();
      let idx: number;
      while ((idx = buffer.indexOf("\n")) >= 0) {
        const line = buffer.slice(0, idx).trim();
        buffer = buffer.slice(idx + 1);
        if (!line) continue;
        let msg: any;
        try {
          msg = JSON.parse(line);
        } catch (err) {
          cleanup();
          reject(err);
          return;
        }

        if (msg.id === 1 && !initialized) {
          initialized = true;
          send({ jsonrpc: "2.0", method: "initialized", params: {} });
          send({ jsonrpc: "2.0", id: 2, method, params });
          toolCallSent = true;
          continue;
        }

        if (msg.id === 2 && toolCallSent) {
          cleanup();
          if (msg.error) {
            logLine(`tool_error method=${method} error=${msg.error.message ?? "unknown"}`);
            reject(new Error(msg.error.message ?? "MCP tool error"));
            return;
          }
          logLine(`tool_ok method=${method}`);
          resolve(msg.result);
          return;
        }
      }
    });

    socket.on("error", (err) => {
      logLine(`socket_error method=${method} error=${err.message}`);
      cleanup();
      reject(err);
    });

    socket.on("close", () => {
      if (!toolCallSent) {
        logLine(`socket_close_no_response method=${method}`);
        reject(new Error("MCP connection closed before response"));
      }
    });
  });
}


function formatContent(result: any) {
  if (result?.content && Array.isArray(result.content)) {
    const text = result.content
      .map((item: any) => (item?.type === "text" ? item.text : JSON.stringify(item)))
      .join("\n");
    return text || JSON.stringify(result);
  }
  return JSON.stringify(result, null, 2);
}

export default function (pi: ExtensionAPI) {
  for (const tool of MCP_TOOLS) {
    pi.registerTool({
      name: tool.name,
      label: tool.name,
      description: tool.description,
      parameters: Type.Object({}, { additionalProperties: true }),
      async execute(_toolCallId, params) {
        logLine(`tool_call name=${tool.name}`);
        const result = await mcpRequest(SOCKET_PATH, "tools/call", {
          name: tool.name,
          arguments: params,
        });
        return {
          content: [{ type: "text", text: formatContent(result) }],
          details: { mcp: result },
        };
      },
    });
  }
}
