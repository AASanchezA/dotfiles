require('minuet').setup({
  virtualtext = {
    -- Set to {} to disable auto-triggering for all filetypes.
    -- You can then manually trigger using 'next' or 'prev' keys (e.g., <A-r>).
    auto_trigger_ft = {},
    keymap = {
      -- Use Alt+a to accept the entire completion
      accept = '<A-a>',
      -- Use Alt+A to accept only the current line
      accept_line = '<A-A>',
      -- Use Alt+r to cycle to the next suggestion (also manually triggers if none)
      next = '<A-r>',
      -- Use Alt+[ to cycle to the previous suggestion
      prev = '<A-[>',
      -- Use Alt+e to dismiss the current suggestion
      dismiss = '<A-e>',
    },
    show_on_completion_menu = true,
  },
  provider = 'openai_fim_compatible',
  provider_options = {
    openai_fim_compatible = {
      api_key = 'TERM',
      name = 'Ollama',
      end_point = 'http://localhost:11434/v1/completions',
      model = 'qwen2.5-coder:7b', -- Supports FIM (Fill-In-the-Middle)
      optional = {
        max_tokens = 256,
        top_p = 0.9,
      },
    },
  },
})
