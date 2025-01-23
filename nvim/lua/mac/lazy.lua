local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        "git",
        "clone",
        "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git",
        "--branch=stable", -- latest stable release
        lazypath,
    })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
    { "folke/which-key.nvim" },
    {
        'nvim-telescope/telescope.nvim',
        tag = '0.1.6',
        -- or                              , branch = '0.1.x',
        dependencies = { 'nvim-lua/plenary.nvim' }

    },
    { 'rose-pine/neovim' },
    { "ellisonleao/gruvbox.nvim" },
    { "nvim-treesitter/nvim-treesitter", build = ":TSUpdate" },
    { 'nvim-treesitter/playground' },
    { 'mbbill/undotree' },
    { 'tpope/vim-fugitive' },
    {
        'NeogitOrg/neogit',
        dependencies = {
            { 'nvim-lua/plenary.nvim' },
            { 'sindrets/diffview.nvim' },
            { 'nvim-telescope/telescope.nvim' },
        },
        config = true
    },
    {
        'VonHeikemen/lsp-zero.nvim',
        dependencies = {
            -- LSP Support
            { 'neovim/nvim-lspconfig' },
            { 'williamboman/mason.nvim' },
            { 'williamboman/mason-lspconfig.nvim' },

            -- Autocompletion
            { 'hrsh7th/nvim-cmp' },
            { 'hrsh7th/cmp-buffer' },
            { 'hrsh7th/cmp-path' },
            { 'saadparwaiz1/cmp_luasnip' },
            { 'hrsh7th/cmp-nvim-lsp' },
            { 'hrsh7th/cmp-nvim-lua' },

            -- Snippets
            { 'L3MON4D3/LuaSnip' },
            { 'rafamadriz/friendly-snippets' },
        }
    },

    {
        'numToStr/Comment.nvim',
        config = function()
            require('Comment').setup()
        end
    },

    {
        'nvim-lualine/lualine.nvim',
        dependencies = { 'kyazdani42/nvim-web-devicons', opt = true }
    },


    {
        "ahmedkhalf/project.nvim",
        config = function()
            require("project_nvim").setup {}
        end

    },
    { "catppuccin/nvim", name = "catppuccin", priority = 1000 },
    { "sainnhe/everforest" },
    { "sainnhe/gruvbox-material" },
    {
      "olimorris/codecompanion.nvim",
      dependencies = {
        "nvim-lua/plenary.nvim",
        "nvim-treesitter/nvim-treesitter",
        "hrsh7th/nvim-cmp", -- Optional: For using slash commands and variables in the chat buffer
        {
          "stevearc/dressing.nvim", -- Optional: Improves the default Neovim UI
          opts = {},
        },
        "nvim-telescope/telescope.nvim", -- Optional: For using slash commands
      },
      config = true
    },
    {
      'claydugo/browsher.nvim',
      event = "VeryLazy",
      config = function()
        -- Specify empty to use below default options
        require('browsher').setup()
      end
    },
    {
      'nvim-lualine/lualine.nvim',
      dependencies = { 'nvim-tree/nvim-web-devicons' }
    }


    -- {
    --   -- "jackMort/ChatGPT.nvim",
    --     dir = "/data/p/github.com/jackMort/ChatGPT.nvim",
    --     event = "VeryLazy",
    --     config = function()
    --       require("chatgpt").setup({
    --           api_host_cmd = "echo https://api.siemens.com/llm",
    --           api_key_cmd = "pass api.siemens.com/llm2",
    --           -- this config assumes you have OPENAI_API_KEY environment variable set
    --           openai_params = {
    --             -- NOTE: model can be a function returning the model name
    --             -- this is useful if you want to change the model on the fly
    --             -- using commands
    --             -- Example:
    --             -- model = function()
    --             --     if some_condition() then
    --             --         return "gpt-4-1106-preview"
    --             --     else
    --             --         return "gpt-3.5-turbo"
    --             --     end
    --             -- end,
    --             model = "starcoder2-3b",
    --             frequency_penalty = 0,
    --             presence_penalty = 0,
    --             max_tokens = 4095,
    --             temperature = 0.2,
    --             top_p = 0.1,
    --             n = 1,
    --           },
    --           openai_edit_params = {
    --             model = "starcoder2-3b",
    --             frequency_penalty = 0,
    --             presence_penalty = 0,
    --             temperature = 0,
    --             top_p = 1,
    --             n = 1,
    --           }
    --         })
    --     end,
    --     dependencies = {
    --       "MunifTanjim/nui.nvim",
    --       "nvim-lua/plenary.nvim",
    --       "folke/trouble.nvim",
    --       "nvim-telescope/telescope.nvim"
    --     }
    -- }
    -- {
    --   "zbirenbaum/copilot.lua",
    --   cmd = "Copilot",
    --   event = "insertenter",
    -- }
})
