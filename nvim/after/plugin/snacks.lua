local snacks = require("snacks")

snacks.setup({
    opts = {
        gh = {
            enabled = true,
            -- Add any gh-specific configurations if needed
        },
        picker = {
            enabled = true,
            sources = {
                gh_issue = {
                    -- gh_issue-specific configurations
                },
                gh_pr = {
                    -- gh_pr-specific configurations
                },
            },
        },
    }
})
