-- Small terminal editor: native file tree plus one optional file picker.
vim.g.mapleader = ' '
vim.opt.number = true
vim.opt.mouse = 'a'
vim.opt.clipboard = 'unnamedplus'
vim.opt.termguicolors = true
vim.opt.ignorecase = true
vim.opt.smartcase = true
vim.opt.splitright = true
vim.opt.splitbelow = true
vim.opt.scrolloff = 4
vim.opt.expandtab = true
vim.opt.shiftwidth = 2
vim.opt.tabstop = 2

-- Netrw is bundled with Neovim. Display a compact sidebar tree.
vim.g.netrw_banner = 0
vim.g.netrw_liststyle = 3
vim.g.netrw_winsize = 25
vim.g.netrw_browse_split = 0

-- `nvim .` normally opens a full-window browser. Start a real sidebar instead.
vim.api.nvim_create_autocmd('VimEnter', {
  group = vim.api.nvim_create_augroup('DotfilesDirectorySidebar', { clear = true }),
  callback = function()
    if vim.fn.argc() ~= 1 or vim.fn.isdirectory(vim.fn.argv(0)) ~= 1 then
      return
    end
    local directory = vim.fn.fnamemodify(vim.fn.argv(0), ':p')
    vim.cmd('enew')
    vim.cmd('Lexplore ' .. vim.fn.fnameescape(directory))
  end,
})

local map = vim.keymap.set
map({ 'n', 'i', 'x' }, '<C-s>', '<Esc><Cmd>write<CR>', { desc = 'Save file' })
map('x', '<C-c>', '"+y', { desc = 'Copy selection' })
map('x', '<C-x>', '"+d', { desc = 'Cut selection' })
map('n', '<C-v>', '"+p', { desc = 'Paste clipboard' })
map('i', '<C-v>', '<C-r><C-o>+', { desc = 'Paste clipboard' })
-- Use the black-hole register so replacing text preserves the clipboard.
map('x', '<C-v>', '"_d"+P', { desc = 'Replace selection with clipboard' })
map('n', '<C-z>', '<Cmd>undo<CR>', { desc = 'Undo' })
map('i', '<C-z>', '<Esc><Cmd>undo<CR>', { desc = 'Undo' })
map('n', '<leader>e', '<Cmd>Lexplore<CR>', { desc = 'Toggle file tree' })
map('n', '<leader><Right>', '<Cmd>vertical resize +5<CR>', { desc = 'Widen current window' })
map('n', '<leader><Left>', '<Cmd>vertical resize -5<CR>', { desc = 'Narrow current window' })
map('n', '<leader><Up>', '<Cmd>resize +2<CR>', { desc = 'Increase window height' })
map('n', '<leader><Down>', '<Cmd>resize -2<CR>', { desc = 'Decrease window height' })

local has_picker, pick = pcall(require, 'mini.pick')
if has_picker then
  pick.setup()
end
map('n', '<leader>f', function()
  if not has_picker then
    vim.notify('Install mini.pick using the README instructions, then restart Neovim.', vim.log.levels.WARN)
    return
  end
  pick.builtin.cli({ command = { 'rg', '--files', '--hidden', '--glob', '!.git', '--color=never' } },
    { source = { name = 'Files' } })
end, { desc = 'Find files in working directory' })
