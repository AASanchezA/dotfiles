local neogit = require('neogit')
neogit.setup {}
vim.keymap.set("n", "<space>gs", vim.cmd.Neogit)
