require'nvim-treesitter.configs'.setup {
  highlight = {
    ensure_installed = {"c", "cpp", "lua", "rust", "go", "bash"},
    sync_install = false,
    auto_install = true,

    enable = true,

    disable = { "python" },
  }
}
