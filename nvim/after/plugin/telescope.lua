local builtin = require('telescope.builtin')
vim.keymap.set('n', '<space>fp', builtin.find_files, { desc = 'Search Files' })
vim.keymap.set('n', '<space>pf', builtin.git_files, { desc = 'Search Git FIles'})
vim.keymap.set('n', '<space>sw', builtin.grep_string, { desc = '[S]earch current [W]ord' })

vim.keymap.set('n', '<space>sp', builtin.live_grep, { desc = '[S]earch by [G]rep' })
vim.keymap.set('n', '<space>bb', builtin.buffers, {})
vim.keymap.set('n', '<space>hh', builtin.help_tags, { desc = '[S]earch [H]elp' })
vim.keymap.set('n', '<space>hk', builtin.keymaps, {})
vim.keymap.set('n', '<space>hc', builtin.commands, {})

vim.keymap.set('n', '<space>sd', builtin.diagnostics, { desc = '[S]earch [D]iagnostics' })


--[[ vim.keymap.set("n", "<space>gs", ":GFiles?<CR>") ]]
--[[ vim.keymap.set("n", "<space>pf", builtin.git_files, {}) ]]
-- vim.keymap.set("n", "<space>ff", ":Files .<CR>")
-- vim.keymap.set("n", "<space>fh", ":History<CR>")
-- vim.keymap.set("n", "<space>fL", ":Locate .<CR>")
-- vim.keymap.set("n", "<space>sp", ":Rg<CR>")
-- vim.keymap.set("n", "<space>sb", ":Lines<CR>")
-- vim.keymap.set("n", "<space>bb", builtin.buffers, {})
-- vim.keymap.set("n", "<space>hh", ":Helptags<CR>")
-- vim.keymap.set("n", "<space>hc", ":Maps<CR>")

