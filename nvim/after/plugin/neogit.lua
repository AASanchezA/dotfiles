local neogit = require('neogit')
neogit.setup {
    kind = "vsplit"
}
-- vim.keymap.set("n", "<space>gs", vim.cmd.Neogit)
vim.keymap.set("n", "<space>gs", function()
    neogit.open({kind = "vsplit"})
end, { desc = "neogit status" })

-- vim.keymap.set("n", "<leader>gs", function()
-- 	neogit.open({ cwd = "%:p:h", kind = "vsplit" })
-- end, { desc = "neogit-status" })
