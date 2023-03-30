vim.g.mapleader = ","
vim.keymap.set("n", "<space>pt", vim.cmd.Ex)

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
