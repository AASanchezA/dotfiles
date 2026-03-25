require('minuet').setup({
  virtualtext = {
    -- Auto-trigger ghost text in these filetypes. You can add more as needed.
    auto_trigger_ft = { 'lua', 'python', 'javascript', 'typescript', 'rust', 'go', 'c', 'cpp', 'html', 'css' },
    keymap = {
      -- Use Alt+A to accept the entire completion
      accept = '<A-A>',
      -- Use Alt+a to accept only the current line
      accept_line = '<A-a>',
      -- Use Alt+] to cycle to the next suggestion
      next = '<A-]>',
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
