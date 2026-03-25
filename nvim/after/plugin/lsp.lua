-- local lsp = require('lsp-zero')
--
-- lsp.preset('recommended')

local lsp = vim.lsp


local cmp = require('cmp')

local cmp_select = { behavior = cmp.SelectBehavior.Select }
cmp.setup( {
  performance = {
    fetching_timeout = 2000,
  },
  snippet = {
    expand = function(args)
      require('luasnip').lsp_expand(args.body)
    end,
  },
  sources = cmp.config.sources({
    { name = 'nvim_lsp' },
    { name = 'minuet' },
  }, {
    { name = 'buffer' },
  }, {
    { name = 'path' },
  }, {
    { name = 'codecompanion_variables' },
  }, {
    { name = 'codecompanion_tools' },
  }
  ),
  formatting = {
    format = function(entry, vim_item)
      if entry.source.name == 'minuet' then
        vim_item.kind = '󱜙 Minuet'
      end
      return vim_item
    end,
  },
  mapping = cmp.mapping.preset.insert({
    ['<C-p>'] = cmp.mapping.select_prev_item(cmp_select),
    ['<C-n>'] = cmp.mapping.select_next_item(cmp_select),
    ['<C-y>'] = cmp.mapping.confirm({ select = true }),
    ['<C-Space>'] = cmp.mapping.complete(),
    ['<A-y>'] = require('minuet').make_cmp_map(),
    })
})

-- cmp.setup({
    -- snippet = {
    --   -- REQUIRED - you must specify a snippet engine
    --   expand = function(args)
    --     vim.fn["vsnip#anonymous"](args.body) -- For `vsnip` users.
    --     -- require('luasnip').lsp_expand(args.body) -- For `luasnip` users.
    --     -- require('snippy').expand_snippet(args.body) -- For `snippy` users.
    --     -- vim.fn["UltiSnips#Anon"](args.body) -- For `ultisnips` users.
    --     -- vim.snippet.expand(args.body) -- For native neovim snippets (Neovim v0.10+)
    --
    --     -- For `mini.snippets` users:
    --     -- local insert = MiniSnippets.config.expand.insert or MiniSnippets.default_insert
    --     -- insert({ body = args.body }) -- Insert at cursor
    --     -- cmp.resubscribe({ "TextChangedI", "TextChangedP" })
    --     -- require("cmp.config").set_onetime({ sources = {} })
    --   end,
    -- },
    -- window = {
    --   -- completion = cmp.config.window.bordered(),
    --   -- documentation = cmp.config.window.bordered(),
    -- },
    -- mapping = cmp.mapping.preset.insert({
    --   ['<C-b>'] = cmp.mapping.scroll_docs(-4),
    --   ['<C-f>'] = cmp.mapping.scroll_docs(4),
    --   ['<C-Space>'] = cmp.mapping.complete(),
    --   ['<C-e>'] = cmp.mapping.abort(),
    --   ['<CR>'] = cmp.mapping.confirm({ select = true }), -- Accept currently selected item. Set `select` to `false` to only confirm explicitly selected items.
    -- }),
    -- sources = cmp.config.sources({
    --   { name = 'nvim_lsp' },
    --   { name = 'vsnip' }, -- For vsnip users.
    --   -- { name = 'luasnip' }, -- For luasnip users.
    --   -- { name = 'ultisnips' }, -- For ultisnips users.
    --   -- { name = 'snippy' }, -- For snippy users.
    -- }, {
    --   { name = 'buffer' },
    -- })
-- })

-- local cmp_mappings = lsp.defaults.cmp_mappings({
-- })


 vim.api.nvim_create_autocmd('LspAttach', {
  group = vim.api.nvim_create_augroup('UserLspConfig', {}),
  callback = function(ev)
    local opts = {buffer = ev.buf, remap = false}

    vim.keymap.set("n", "<leader>gd", function() vim.lsp.buf.definition() end, opts)
    vim.keymap.set("n", "<leader>gg", function() vim.lsp.buf.definition() end, opts)
    vim.keymap.set("n", "K", function() vim.lsp.buf.hover() end, opts)
    vim.keymap.set("n", "<C-k>", function() vim.lsp.buf.signature_help() end, opts)
    vim.keymap.set("n", "<leader>gca", function() vim.lsp.buf.code_action() end, opts)
    vim.keymap.set("n", "<leader>gr", function() vim.lsp.buf.references() end, opts)
    vim.keymap.set("n", "<leader>gcr", function() vim.lsp.buf.rename() end, opts)
    vim.keymap.set("n", "<C-h>", function() vim.lsp.buf.signature_help() end, opts)
    vim.keymap.set("n", "<leader>gws", function() vim.lsp.buf.workspace_symbol() end, opts)
    vim.keymap.set("n", "<leader>ge", function() vim.diagnostic.open_float() end, opts)
    vim.keymap.set("n", "[d", function() vim.diagnostic.goto_next() end, opts)
    vim.keymap.set("n", "]d", function() vim.diagnostic.goto_prev() end, opts)

    vim.keymap.set("n", "<leader>gi", function() vim.lsp.buf.implementation() end, opts)
    vim.keymap.set("n", "<leader>gtd", function() vim.lsp.buf.type_definition() end, opts)
    vim.keymap.set("n", "<leader>==", function() vim.lsp.buf.format() end, opts)


    --#region
    --#region
    --
    -- Create a command `:Format` local to the LSP buffer
    vim.api.nvim_buf_create_user_command(ev.buf, 'Format', function(_)
        if vim.lsp.buf.format then
            vim.lsp.buf.format()
        elseif vim.lsp.buf.formatting then
            vim.lsp.buf.formatting()
        end
    end, { desc = 'Format current buffer with LSP' })
  end
 })


-- lsp.client.on_attach(function(client, bufnr)
--     local opts = {buffer = bufnr, remap = false}
--
--     vim.keymap.set("n", "<leader>gd", function() vim.lsp.buf.definition() end, opts)
--     vim.keymap.set("n", "<leader>gg", function() vim.lsp.buf.definition() end, opts)
--     vim.keymap.set("n", "K", function() vim.lsp.buf.hover() end, opts)
--     vim.keymap.set("n", "<C-k>", function() vim.lsp.buf.signature_help() end, opts)
--     vim.keymap.set("n", "<leader>gca", function() vim.lsp.buf.code_action() end, opts)
--     vim.keymap.set("n", "<leader>gr", function() vim.lsp.buf.references() end, opts)
--     vim.keymap.set("n", "<leader>gcr", function() vim.lsp.buf.rename() end, opts)
--     vim.keymap.set("n", "<C-h>", function() vim.lsp.buf.signature_help() end, opts)
--     vim.keymap.set("n", "<leader>gws", function() vim.lsp.buf.workspace_symbol() end, opts)
--     vim.keymap.set("n", "<leader>ge", function() vim.diagnostic.open_float() end, opts)
--     vim.keymap.set("n", "[d", function() vim.diagnostic.goto_next() end, opts)
--     vim.keymap.set("n", "]d", function() vim.diagnostic.goto_prev() end, opts)
--
--     vim.keymap.set("n", "<leader>gi", function() vim.lsp.buf.implementation() end, opts)
--     vim.keymap.set("n", "<leader>gtd", function() vim.lsp.buf.type_definition() end, opts)
--     vim.keymap.set("n", "<leader>==", function() vim.lsp.buf.formatting() end, opts)
--
--
--     --#region
--     --#region
--     --
--     -- Create a command `:Format` local to the LSP buffer
--     vim.api.nvim_buf_create_user_command(bufnr, 'Format', function(_)
--         if vim.lsp.buf.format then
--             vim.lsp.buf.format()
--         elseif vim.lsp.buf.formatting then
--             vim.lsp.buf.formatting()
--         end
--     end, { desc = 'Format current buffer with LSP' })
-- end)
--
-- lsp.setup()

require('mason').setup({})
require('mason-lspconfig').setup({
    ensure_installed = {
        'ts_ls',
        'eslint',
        'lua_ls',
        'rust_analyzer',
        'pyright',
        'clangd',
        'gopls'
    },
  handlers = {
    -- lsp.default_setup,
  },
})



vim.diagnostic.config({
  virtual_text = true,
  signs = true,
  update_in_insert = false,
  underline = true,
  severity_sort = false,
  float = true,
})

vim.lsp.config("lua_ls", {
  on_init = function(client)
    if client.workspace_folders then
      local path = client.workspace_folders[1].name
      if vim.loop.fs_stat(path..'/.luarc.json') or vim.loop.fs_stat(path..'/.luarc.jsonc') then
        return
      end
    end

    client.config.settings.Lua = vim.tbl_deep_extend('force', client.config.settings.Lua, {
      runtime = {
        -- Tell the language server which version of Lua you're using
        -- (most likely LuaJIT in the case of Neovim)
        version = 'LuaJIT'
      },
      -- Make the server aware of Neovim runtime files
      workspace = {
        checkThirdParty = false,
        library = {
          vim.env.VIMRUNTIME
          -- Depending on the usage, you might want to add additional paths here.
          -- "${3rd}/luv/library"
          -- "${3rd}/busted/library",
        }
        -- or pull in all of 'runtimepath'. NOTE: this is a lot slower and will cause issues when working on your own configuration (see https://github.com/neovim/nvim-lspconfig/issues/3189)
        -- library = vim.api.nvim_get_runtime_file("", true)
      }
    })
  end,
  settings = {
    Lua = {}
  }
})

-- require'lspconfig'.pyright.setup {
--   on_init = function(client)
--     if client.workspace_folders then
--       local path = client.workspace_folders[1].name
--       if vim.loop.fs_stat(path..'/.luarc.json') or vim.loop.fs_stat(path..'/.luarc.jsonc') then
--         return
--       end
--     end
--
--     client.config.settings.Lua = vim.tbl_deep_extend('force', client.config.settings.Lua, {
--       runtime = {
--         -- Tell the language server which version of Lua you're using
--         -- (most likely LuaJIT in the case of Neovim)
--         version = 'LuaJIT'
--       },
--       -- Make the server aware of Neovim runtime files
--       workspace = {
--         checkThirdParty = false,
--         library = {
--           vim.env.VIMRUNTIME
--           -- Depending on the usage, you might want to add additional paths here.
--           -- "${3rd}/luv/library"
--           -- "${3rd}/busted/library",
--         }
--         -- or pull in all of 'runtimepath'. NOTE: this is a lot slower and will cause issues when working on your own configuration (see https://github.com/neovim/nvim-lspconfig/issues/3189)
--         -- library = vim.api.nvim_get_runtime_file("", true)
--       }
--     })
--   end,
--   settings = {
--     Lua = {}
--   }
-- }
