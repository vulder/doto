require'nvim-treesitter.configs'.setup {
  ensure_installed = { 
    "c", "cpp", "lua", "rust", "go", "bash", "llvm",
    "latex", "cmake", "bibtex", "json"
  },
  sync_install = false,
  auto_install = true,

  highlight = {
    enable = true,

    disable = { "python", "yaml", "html" },
  }
}
