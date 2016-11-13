execute pathogen#infect()
set shell=/bin/bash
set autoindent
set smartindent
set tabstop=4
set shiftwidth=4
set wrapmargin=0
set number
set hlsearch
set mouse=a

" Make gvim look like vim (but with nice color support and stuff)
set guioptions-=T
set guioptions-=L
set guioptions-=r
set guioptions-=m
set vb t_vb=
set ruler
set incsearch
set showmatch

" Font and colors
" set guifont=ProFontWindows\ 10
set noanti

" Note: this is only used as a fallback for command line vim, see .gvimrc to
" change colortheme in gvim.
colorscheme molokai

syntax on
filetype on
filetype plugin on
filetype plugin indent on

set lazyredraw

" Lots of history and undo, do not create swapfiles
set history=1000
set undolevels=1000
set wildignore=*.swp,*.bak,*.pyc,*.class,*.so,*.zip
set nobackup
set noswapfile

" Show tabs as >.. and trailing space in different color
" Only enabled in py files or manually with set list
set listchars=tab:>.,trail:\ ,extends:#,nbsp:.

" Remap Ctrl-P start
let g:ctrlp_map = '<C-p>'
let g:ctrlp_cmd = 'CtrlP'

" Move to wrapped line
nnoremap j gj
nnoremap k gk

" Easy window navigation, ctrl+h, j, k, l to move between splits
" Also use Ctrl+arrow-key to navigate.
map <C-h> <C-w>h
map <C-k> <C-w>k
map <C-j> <C-w>j
map <C-l> <C-w>l
map <C-Left>  <C-w>h
map <C-Up>    <C-w>j
map <C-Down>  <C-w>k
map <C-Right> <C-w>l

" Save faster with ctrl+s
map <C-s> :w<Cr>
imap <C-s> :w<Cr>i

" Escape faster, leave insert mode with jj or aa
imap jj <Esc>
imap aa <Esc>

" Smart home - Got to first non-blank character. Unless already there, then go
"              to start of line instead
noremap <expr> <silent> <Home> col('.') == match(getline('.'),'\S')+1 ? '0' : '^'
imap <silent> <Home> <C-O><Home>

" Force save with sudo by using :w!!
cmap w!! w !sudo tee % >/dev/null

" Python
autocmd FileType python set smarttab | set expandtab | set softtabstop=4 | set list
let g:syntastic_python_checkers=['flake8', 'pyflakes']
let g:syntastic_python_flake8_args="--ignore=E501"

" Javascript
autocmd FileType javascript set smarttab | set expandtab | set shiftwidth=4 | set softtabstop=4

" Ruby
autocmd FileType ruby set smarttab | set expandtab | set softtabstop=2 | set shiftwidth=2 | set tabstop=2
autocmd FileType rb colorscheme sift

" Java
autocmd FileType java set makeprg=ant
autocmd FileType java set efm=%A\ %#[javac]\ %f:%l:\ %m,%-Z\ %#[javac]\ %p^,%-C%.%#
autocmd FileType java ab sout System.out.println("");3ha
autocmd FileType java set smarttab | set expandtab | set softtabstop=4
let g:syntastic_java_checkers=[]

" PHP
autocmd FileType php ab ss $_SESSION['
autocmd FileType php ab sg $_GET['
autocmd FileType php ab sp $_POST['

" Sass
au! BufRead,BufNewFile *.scss setfiletype scss

" Less
au BufNewFile,BufRead *.less set filetype=less

" Improve completion menu
set completeopt=longest,menuone
inoremap <expr> <CR> pumvisible() ? "\<C-y>" : "\<C-g>u\<CR>"
inoremap <expr> <C-n> pumvisible() ? '<C-n>' : '<C-n><C-r>=pumvisible() ? "\<lt>Down>" : ""<CR>'

" Paste over a selection without putting selection in copybuffer with t
vmap t "_dP

" Don't show .pyc files in NERDTree
let NERDTreeIgnore=['\.pyc']

" Use Ctrl-P
set runtimepath^=~/.vim/bundle/ctrlp.vim

" Ctags
set tags=~/.vim/ctags

" Other Key mappings
nmap <F1> :!ctags -R --languages=python -o ~/.vim/ctags `pwd`
nmap <F2> :NERDTreeToggle<CR>
nmap <F4> :Gstatus<CR>
" nmap <F5> :Git push

" Yankring on F11, let's you paste stuff you copied earlier
nmap <silent> <F11> :YRShow<CR>

" Fold stuff
nnoremap <space> zA
set foldlevelstart=20

" cd to path of currently open file with ,cd
map ,cd :cd %:p:h<CR>

" Clear search pattern (removes marking by hlsearch)
command C let @/ = ""

" insert {[]} with alt-7,8,9,0 as a complement to alt-gr
imap · {
imap ¸ [
imap ¹ ]
imap ° }

" Make :W work like :w etc. And fix the common typo :Wq
cab Q q
cab W w
cab X x
cab Wq wq

set exrc

" Turn off the colored line, 80 char line, that started showing up after some update.
set colorcolumn=0
set cc=0

" Yankring history directory
let g:yankring_history_dir = "~/.vim_yankring_history"
