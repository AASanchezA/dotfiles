local builtin = require('telescope.builtin')
local actions = require('telescope.actions')

require("telescope").load_extension("projects")

vim.keymap.set('n', '<space>fp', builtin.find_files, { desc = 'Search All Projects Files' })
vim.keymap.set('n', '<space>pf', function() builtin.git_files { cwd='.' } end, { desc = 'Search Projects FIles'})
vim.keymap.set('n', '<space>pp', function() require("telescope").extensions.projects.projects{} end, { desc = 'Search Projects' })
vim.keymap.set('n', '<space>pP', function() builtin.find_files { cwd='~/Proj', find_command = { "fd", "--type", "d", "--color", "never" } } end, { desc = 'Search All Projects' })

vim.keymap.set('n', '<space>fa', function() builtin.find_files { search_dirs={"/"} } end, { desc = 'Search All Files from /'})
vim.keymap.set('n', '<space>fd', function() builtin.find_files { cwd='~/dotfiles' } end, { desc = 'Search dotfiles FIles'})
vim.keymap.set('n', '<space>ff', function() builtin.find_files { search_dirs={"/etc", "/dev", "/lib/systemd/", "~/.config" } } end, { desc = 'Search Config System Files'})
vim.keymap.set('n', '<space>fc', function() builtin.find_files { cwd='~/.config', follow=true } end, { desc = 'Search Local Config FIles'})

vim.keymap.set('n', '<space>sp', builtin.live_grep, { desc = '[S]earch by [G]rep' })

vim.keymap.set('n', '<space>sap', function() builtin.live_grep { search_dirs={ "~/proj"} } end, { desc = '[S]earch by [G]rep [A]ll [P]rojects' })

vim.keymap.set('n', '<space>sw', builtin.grep_string, { desc = '[S]earch current [W]ord' })
vim.keymap.set('n', '<space>sP', function() builtin.grep_string {search=vim.fn.expand("<cword>")} end, { desc = '[S]earch by grep [P]roject with word under cursor' })
vim.keymap.set('n', '<space>sl', builtin.resume , { desc = '[S]earch resume [l]ast search' })
vim.keymap.set('n', '<space>bb', builtin.buffers, { desc = '[B][B]buffers list' })
vim.keymap.set('n', '<space>hh', builtin.help_tags, { desc = '[S]earch [H]elp' })
vim.keymap.set('n', '<space>hk', builtin.keymaps, { desc = '[H]elp [K]eymaps list' })
vim.keymap.set('n', '<space>hc', builtin.commands, {})

vim.keymap.set('n', '<space>el', function() builtin.diagnostics {bufnr=0} end, { desc = '[S]earch [D]iagnostics' })

-- Telescope Git keymaps
vim.keymap.set('n', '<space>gbl', builtin.git_branches, { desc = '[G]it [B]ranch [L]ocal' })
vim.keymap.set('n', '<space>gll', builtin.git_commits, { desc = '[G]it [L]ogs [L]ocal branch' })
vim.keymap.set('n', '<space>glb', builtin.git_bcommits, { desc = '[G]it [L]ogs all [B]ranch' })

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

