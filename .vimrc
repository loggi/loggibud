set nocompatible     		" be iMproved, required
colorscheme desert 		"used to be morning
syntax enable 				"enable syntax processing
filetype indent on  		"load filetype-specific indent files
filetype on
filetype plugin indent on   " required!

set tabstop=2		"number of visual spaces per TAB
set softtabstop=2	"number of spaces when editing (which are inserted when hitting <TAB>
set shiftwidth=2
set expandtab		"tabs become spaces

" Change indentation depending on the file type
autocmd FileType html setlocal shiftwidth=2 tabstop=2 softtabstop=2
autocmd FileType javascript setlocal shiftwidth=2 tabstop=2 softtabstop=2
autocmd FileType css setlocal shiftwidth=2 tabstop=2 softtabstop=2
autocmd FileType python set tabstop=4 softtabstop=4 shiftwidth=4 textwidth=79 expandtab autoindent fileformat=unix
au BufRead,BufNewFile *.tpl set filetype=html "to read Bottle templates as HTML"
"autocmd BufNewFile,BufRead *.py set tabstop=4 softtabstop=4 shiftwidth=4 textwidth=79 expandtab autoindent fileformat=unix

set number		  "show line numbers
set showcmd		  "to show command line at the bottom bar
set cursorline	  "to highlight the current line
set wildmenu      "provides a graphical menu for autocomplete
set lazyredraw    "redraw only when needed
set showmatch     "highlight matching {[()]}

" Add column at the end of a number of characters
set colorcolumn=80
highlight ColorColumn ctermbg=red guibg=red "used to be lightgray

set incsearch       "search as characters are typed
set hlsearch        "highlight matches

set foldenable          "enable folding
set foldlevelstart=10   "open most folds by default (only indentation of level 10 is shown. Come on, I cannot indent more than that)
set foldnestmax=10      "maximum number of nested folders
set foldmethod=indent   "fold based on file type

set directory=$HOME/.vim/swap// " swap files in a specific folder

"" Remaps
" Turn off search highlight after pressing <leader><space> (<leader> by default is '\')
nnoremap <leader><space> :nohlsearch<CR>

" Remap the 'za' folding command to <space>
nnoremap <space> za

" Move vertically by visual line (I added this here but I am not sure if required. So uncomment later if you see fit)
" nnoremap j gj
" nnoremap k gk

" Remap the escape <Esc> key to j followed by k, which is less far away than Esc
inoremap jk <esc>

" Remap the leader key to be space
"let mapleader = '\<Space>'

" To split a line by pressing Ctrl+J. Notice that Shift+J mixes two lines
nnoremap <NL> i<CR><ESC>

" Remap emmet trigger key from <C-Y>, to <C-Z>, (notice we need to press C-Z,
" let go AND then press ,)
let g:user_emmet_leader_key='<C-z>'


" Replace in Visual mode: press Ctrl+r to replace a selected text (useless as I preferred to copy and use Ctrl + R + " to paste in the terminal)
"vnoremap <C-r> "hy:%s/<C-r>h//gc<left><left><left>

"Plugin manager (Vim-plug)
call plug#begin('~/.vim/plugged')

Plug 'mattn/emmet-vim'
Plug 'scrooloose/nerdcommenter'
Plug 'Vimjas/vim-python-pep8-indent'
Plug 'jonsmithers/vim-html-template-literals' 
Plug 'pangloss/vim-javascript'
Plug 'valloric/youcompleteme' "auto-complete without having to type Ctrl + N
Plug 'jiangmiao/auto-pairs'   "auto-close { and stuff, and properly indent when pressing ENTER
Plug 'prettier/vim-prettier'  "This one is definitely not working
Plug 'tpope/vim-fugitive'     "Git commands
Plug 'uarun/vim-protobuf'     "Protobuf syntax and indentation
Plug 'python-mode/python-mode', { 'for': 'python', 'branch': 'develop' } "Make sure pylint is installed in the system
"Plug 'sheerun/vim-polyglot' " I was having some problems with Vue indentation
"Plug 'evanleck/vim-svelte'
"Plug 'leafOfTree/vim-vue-plugin'
Plug 'tweekmonster/django-plus.vim' "Django better handling of templates
Plug 'cespare/vim-toml'  " Support for Toml files
Plug 'vim-latex/vim-latex'  "Latex support

call plug#end()

" Vim vue (uncomment if ever using Vue again)
"let g:vim_vue_plugin_load_full_syntax = 1

" So that html-template-literals works
let g:html_indent_style1 = 'inc'
let g:htl_all_templates = 1 "experimental for template literals

" Let prettier work without having to write //@format at the top of the file
let g:prettier#autoformat_require_pragma = 0

" Latex plugin has a Ctrl+J mapping to something I do not know and do not
" care. Since I use this mapping already, I remapped it to something else
nnoremap <leader>v <Plug>IMAP_JumpForward
