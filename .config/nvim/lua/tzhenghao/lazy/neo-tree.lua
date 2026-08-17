return {
  "nvim-neo-tree/neo-tree.nvim",
  branch = "v3.x",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-tree/nvim-web-devicons",
    "MunifTanjim/nui.nvim",
  },
  lazy = false,
  keys = {
    { "<leader>e", "<cmd>Neotree toggle<cr>", desc = "Neo-tree toggle" },
    { "<leader>o", "<cmd>Neotree focus<cr>", desc = "Neo-tree focus" },
    { "<leader>ge", "<cmd>Neotree float git_status<cr>", desc = "Neo-tree git status" },
    { "<leader>be", "<cmd>Neotree toggle show buffers right<cr>", desc = "Neo-tree buffers" },
  },
  opts = {
    close_if_last_window = true,
    window = { width = 32 },
    filesystem = {
      follow_current_file = { enabled = true },
      use_libuv_file_watcher = true,
      hijack_netrw_behavior = "open_current",
      filtered_items = {
        visible = false,
        hide_dotfiles = false,
        hide_gitignored = true,
      },
    },
  },
}
