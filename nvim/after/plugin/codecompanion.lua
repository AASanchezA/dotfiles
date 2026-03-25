local codecompanion = require("codecompanion")
codecompanion.setup({
    adapters = {
        ollama = function()
            return require("codecompanion.adapters.http").extend("ollama", {
                name = "qwen3:8b", -- Give this adapter a different name to differentiate it from the default ollama adapter
                schema = {
                    model = {
                        default = "qwen3:8b",
            -- default = "qwen2.5-coder:7b",
                        -- default = "gemma3:4b",
                    },
                    num_ctx = {
                        default = 16384,
                    },
                    num_predict = {
                        default = -1,
                    },
                },
            })
        end,
    },
    strategies = {
        inline = { adapter = "ollama", },
        chat = {
            adapter = "ollama",
            slash_commands = {
                ["file"] = {
                    -- Location to the slash command in CodeCompanion
                    callback = "strategies.chat.slash_commands.file",
                    description = "Select a file using Telescope",
                    opts = {
                        provider = "telescope", -- Other options include 'default', 'mini_pick', 'fzf_lua', snacks
                        contains_code = true,
                    },
                },
                ["buffer"] = {
                    -- Location to the slash command in CodeCompanion
                    callback = "strategies.chat.slash_commands.buffer",
                    description = "Select a buffer using Telescope",
                    opts = {
                        provider = "telescope",   -- Other options include 'default', 'mini_pick', 'fzf_lua', snacks
                        contains_code = true,
                    },
                },
                ["symbols"] = {
                    callback = "strategies.chat.slash_commands.symbols",
                    description = "Select symbols using Telescope",
                    opts = {
                        provider = "telescope",
                    },
                },
                ["help"] = {
                    callback = "strategies.chat.slash_commands.help",
                    description = "Select help tags using Telescope",
                    opts = {
                        provider = "telescope",
                    },
                },
            },
        },
    },
    display = {
        action_palette = {
            width = 95,
            height = 10,
            prompt = "Prompt ",             -- Prompt used for interactive LLM calls
            provider = "telescope",         -- default|telescope|mini_pick
            opts = {
                show_default_actions = true, -- Show the default actions in the action palette?
                show_default_prompt_library = true, -- Show the default prompt library in the action palette?
            },
        },
        diff = {
            provider = "default", -- default|mini_diff
        },
    }
})

-- Keymaps
vim.keymap.set({ "n", "v" }, "<leader>gsa", "<cmd>CodeCompanionActions<cr>", { noremap = true, silent = true, desc = "CodeCompanion Actions" })
vim.keymap.set({ "n", "v" }, "<leader>gsc", "<cmd>CodeCompanionChat Toggle<cr>", { noremap = true, silent = true, desc = "CodeCompanion Chat" })
vim.keymap.set({ "n", "v" }, "<leader>gsi", "<cmd>CodeCompanion<cr>", { noremap = true, silent = true, desc = "CodeCompanion Inline" })
vim.keymap.set("v", "ga", "<cmd>CodeCompanionChat Add<cr>", { noremap = true, silent = true, desc = "Add to CodeCompanion Chat" })

-- Expand 'cc' into 'CodeCompanion' in the command line
vim.cmd([[cab ccc CodeCompanion]])
