vim.g.mapleader = ","
vim.keymap.set("n", "<space>pt", vim.cmd.Vex)

-- Move blocks around
vim.keymap.set("v", "<C-j>", ":m '>+1<CR>gv=gv")
vim.keymap.set("v", "<C-k>", ":m '<-2<CR>gv=gv")

-- change current dir
-- TODO test which one is better :cd or :lcd which change cwd for buffer
vim.keymap.set("n", "<space>cd", ":cd %:p:h<CR>:pwd<CR>")

-- Keep in the middle
vim.keymap.set("n", "J", "mzJ`z")
vim.keymap.set("n", "<C-d>", "<C-d>zz")
vim.keymap.set("n", "<C-u>", "<C-u>zz")
vim.keymap.set("n", "n", "nzzzv")
vim.keymap.set("n", "N", "Nzzzv")

-- keep copy
vim.keymap.set("x", "<leader>p", "\"_dP")

-- copy to clipboard
vim.keymap.set("n", "<leader>y", "\"+y")
vim.keymap.set("v", "<leader>y", "\"+y")
vim.keymap.set("n", "<leader>Y", "\"+Y")

-- delete to /dev/null
vim.keymap.set("n", "<leader>d", "\"_d")
vim.keymap.set("v", "<leader>d", "\"_d")

-- clean search
vim.keymap.set("n", "<CR><CR>", ":noh<CR><CR>")

-- from old vimrc
-- remap to save file with ctr+s
vim.keymap.set("i", "<C-s>", "<esc>:w<cr>")
vim.keymap.set("n", "<C-s>", ":w<cr>")

vim.keymap.set("v", "<", "<gv")
vim.keymap.set("v", ">", ">gv")

-- fast togle between last/current buffer 
vim.keymap.set("n", "<space><tab>",  "<C-^>")
-- Buffers - explore/next/previous: 
vim.keymap.set("n", "<space>bn",   ":bn<CR>")
vim.keymap.set("n", "<space>bp",   ":bp<CR>")

-- Open from the latest commit, the recommended default operation
vim.keymap.set('n', '<leader>bb', '<cmd>Browsher commit<CR>', { noremap = true, silent = true })
vim.keymap.set('v', '<leader>bb', ":'<,'>Browsher commit<CR>gv", { noremap = true, silent = true })

-- Open from the latest tag, for more human readable urls (with risk of outdated line numbers)
vim.keymap.set('n', '<leader>BB', '<cmd>Browsher tag<CR>', { noremap = true, silent = true })
vim.keymap.set('v', '<leader>BB', ":'<,'>Browsher tag<CR>gv", { noremap = true, silent = true })

-- quickfix list
-- vim.keymap.set("n", "<C-k>", "<cmd>cnext<CR>zz")
-- vim.keymap.set("n", "<C-j>", "<cmd>cprev<CR>zz")

-- Highlight when yanking (copying) text
--  Try it with `yap` in normal mode
--  See `:help vim.highlight.on_yank()`
vim.api.nvim_create_autocmd('TextYankPost', {
  desc = 'Highlight when yanking (copying) text',
  group = vim.api.nvim_create_augroup('kickstart-highlight-yank', { clear = true }),
  callback = function()
    vim.highlight.on_yank()
  end,
})
