"enable pathogen"
execute pathogen#infect()

"enable autocomplete"
let g:neocomplete#enable_at_startup = 1

" AutoComplPop like behavior. "
let g:neocomplete#enable_auto_select = 1

" Add spaces after comment delimiters by default
let g:NERDSpaceDelims = 1

set background=dark
let g:solarized_termcolors=256
colorscheme solarized

syntax enable
set guifont=Monaco:h12

"Display number lines"
set number

"enable 256 colors"
set t_Co=256

"Automatically load the file if it is modified"
set autoread

"no backup file - just use git"
set nobackup

"Disable the swap file"
set noswapfile

"Always show status line"
set laststatus=2

"Indent settings"
set tabstop=4
set shiftwidth=4
set smartindent
set expandtab

"Set the ruler to 80 columns"
set colorcolumn=80

"Ignore case in search patterns"
set ignorecase

"Keep at least 3 lines above/below"
set scrolloff=3

"Show immediately where the so-far typed pattern matches."
set incsearch

"Highlight search term"
set hlsearch

"Always show the status of the file"
set laststatus=2

set lazyredraw

"Control-s to save"
:nmap <c-s> :w<CR>
:imap <c-s> <Esc>:w<CR>a
:imap <c-s> <Esc><c-s>

"When we hit enter, a new line is created on top/bottom without moving"
"the cursor."
nmap <S-Enter> O<Esc>
nmap <CR> o<Esc>

"This shifts the lines up or down"
nnoremap <S-j> :m .+1<CR>==
nnoremap <S-k> :m .-2<CR>==
vnoremap <S-j> :m '>+1<CR>gv=gv
vnoremap <S-k> :m '<-2<CR>gv=gv

"This shifts the lines up or down"
nnoremap <A-j> :m .+1<CR>==
nnoremap <A-k> :m .-2<CR>==
inoremap <A-j> <Esc>:m .+1<CR>==gi
inoremap <A-k> <Esc>:m .-2<CR>==gi
vnoremap <A-j> :m '>+1<CR>gv=gv
vnoremap <A-k> :m '<-2<CR>gv=gv

"This swaps tabs in Vim"
nnoremap tk :tabn<CR>
nnoremap tj :tabp<CR>
nnoremap tn :tabe<CR>

"Remap ; to : in normal mode - More efficient!"
nnoremap ; :

"find using f"
nmap f /

"Remap Vim 0 to first non-blank char"
nmap 0 ^
