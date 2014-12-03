" An example for a vimrc file.
"
" Maintainer:	Andres Sanchez <andres-sanchez@gmx.net>
" Last change:	2013 Nov 27
"
" To use it, copy it to
"     for Unix and OS/2:  ~/.vimrc
"	      for Amiga:  s:.vimrc
"  for MS-DOS and Win32:  $VIM\_vimrc
"	    for OpenVMS:  sys$login:.vimrc

" When started as "evim", evim.vim will already have done these settings.
if v:progname =~? "evim"
  finish
endif

"=================================================================
"=================== Start keybinding ============================
"for learning vim I'm going to disable my arrows keys
"Hoppefully I will learno some time to program
"=================================================================
no   <down>    <Nop>
no   <left>    <Nop>
no   <right>   <Nop>
no   <up>      <Nop>

ino   <down>    <Nop>
ino   <left>    <Nop>
ino   <right>   <Nop>
ino   <up>      <Nop>

" Use Vim settings, rather than Vi settings (much better!).
" This must be first, because it changes other options as a side effect.
set nocompatible

"Automatic reloading of .vimrc
autocmd! bufwritepost .vimrc source %

"TODO Better copy & paste
"set pastetoggle=<F2>
"set clipboard=unnamed

" Setting tab size
set ts=4

" allow backspacing over everything in insert mode
set backspace=indent,eol,start

if has("vms")
  set nobackup		" do not keep a backup file, use versions instead
else
  set backup		" keep a backup file
endif
set history=50		" keep 50 lines of command line history
set ruler		" show the cursor position all the time
set showcmd		" display incomplete commands
set incsearch		" do incremental searching

" For Win32 GUI: remove 't' flag from 'guioptions': no tearoff menu entries
" let &guioptions = substitute(&guioptions, "t", "", "g")


" CTRL-U in insert mode deletes a lot.  Use CTRL-G u to first break undo,
" so that you can undo CTRL-U after inserting a line break.
"inoremap <C-U> <C-G>u<C-U>

" setting guifont
if has('gui_running')
  set guifont=Monospace\ 10
endif

" In many terminal emulators the mouse works just fine, thus enable it.
if has('mouse')
  set mouse=a
endif

" Switch syntax highlighting on, when the terminal has colors
" Also switch on highlighting the last used search pattern.
syntax on
"if &t_Co > 2 || has("gui_running")
set hlsearch
"endif

" Only do this part when compiled with support for autocommands.
if has("autocmd")

  " Enable file type detection.
  " Use the default filetype settings, so that mail gets 'tw' set to 72,
  " 'cindent' is on in C files, etc.
  " Also load indent files, to automatically do language-dependent indenting.
  filetype plugin indent on

  " Put these in an autocmd group, so that we can delete them easily.
  augroup vimrcEx
  au!

  " For all text files set 'textwidth' to 78 characters.
  autocmd FileType text setlocal textwidth=78

  " When editing a file, always jump to the last known cursor position.
  " Don't do it when the position is invalid or when inside an event handler
  " (happens when dropping a file on gvim).
  " Also don't do it when the mark is in the first line, that is the default
  " position when opening a file.
  autocmd BufReadPost *
    \ if line("'\"") > 1 && line("'\"") <= line("$") |
    \   exe "normal! g`\"" |
    \ endif

  augroup END

else

  set autoindent		" always set autoindenting on

endif " has("autocmd")

" Convenient command to see the difference between the current buffer and the
" file it was loaded from, thus the changes you made.
" Only define it when not defined already.
if !exists(":DiffOrig")
  command DiffOrig vert new | set bt=nofile | r ++edit # | 0d_ | diffthis
		  \ | wincmd p | diffthis
endif


"=================================================================
"=================== Setting Up Tab size  ========================
"=================================================================
set smartindent
set noexpandtab
set copyindent
set preserveindent
set softtabstop=0
set shiftwidth=4
set tabstop=4

"=================================================================
"=================== Setting Up temp file ========================
"=================================================================
" controls where backup files (with ~ extension by default) go.
set backupdir=~/.vim/vimtmp

" The 'directory' option controls where swap files go.
set directory=~/.vim/vimtmp

"=================================================================
"=================== Useful Keybindings ==========================
"=================================================================
"This unsets the "last search pattern" register by hitting return
nnoremap <CR><CR> :noh<CR><CR>

"remap to save file with ctr+s
inoremap <C-s> <esc>:w<cr>a
nnoremap <C-s> :w<cr>a

"set mapleader to comma key
let mapleader=","

imap ii <Esc>

" Bubble single lines
nmap <C-k> [e
nmap <C-j> ]e
" Bubble multiple line
vmap <C-k> [egv
vmap <C-j> ]egv

"Indent code between braces
"map <C-f> gq 

" remaping square brackets
nnoremap ü <]>
nnoremap Ü <[>

" Easier moving of code Blocks
" better indetation
vnoremap < <gv 
vnoremap > >gv

"Map Bufplorer to be control by <ALT> pageUp and pageDown
" Buffers - explore/next/previous: 
"nnoremap <C-F12>      :BufExplorer<CR> 
nnoremap <leader>bb   :buffers<CR>
nnoremap <leader>bn   :bn<CR>
nnoremap <leader>bm   :bp<CR>
" easier moving between tabs
map <Leader>n <esc>:tabprevious<CR>
map <Leader>m <esc>:tabnext<CR>


"=================================================================
"=================== NerdTree Settings ===========================
"=================================================================
"How can I open a NERDTree automatically when vim starts up?
"autocmd vimenter * NERDTree

"How can I open a NERDTree automatically when vim starts up if no files were specified?
autocmd vimenter * if !argc() | NERDTree | endif

"How can I map a specific key or shortcut to open NERDTree?
"open NERDTree with Ctrl+n (you can set whatever key you want):
 map <C-n> :NERDTreeToggle<CR>

"How can I close vim if the only window left open is a NERDTree?
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTreeType") && b:NERDTreeType == "primary") | q | endif

"=================================================================
"=================== Pathogen Packages Manager ===================
"=================================================================
"pathogen.vim
"Manage your 'runtimepath' with ease. In practical terms, pathogen.vim makes
"it super easy to install plugins and runtime files in their own private
"directories
execute pathogen#infect()

"vundle setup
set nocompatible               " be iMproved
filetype off                   " required!

"Bundle 'fuzzyfinder'
" git repos on your local machine (ie. when working on your own plugin)
"Bundle 'file:///Users/gmarik/path/to/plugin'
" ...
filetype plugin indent on     " required!

" Brief help
" :BundleList          - list configured bundles
" :BundleInstall(!)    - install(update) bundles
" :BundleSearch(!) foo - search(or refresh cache first) for foo
" :BundleClean(!)      - confirm(or auto-approve) removal of unused bundles
"
" see :h vundle for more details or wiki for FAQ
" NOTE: comments after Bundle command are not allowed..

set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

" let Vundle manage Vundlewurden gerne dabei sein
" required! 
Bundle 'gmarik/vundle'

"=================================================================
"=================== My Vim Plugins ==============================
"=================================================================
" My Bundles here:
"original repos on github
Bundle 'Valloric/YouCompleteMe.git'
Bundle 'tpope/vim-fugitive'
Bundle 'Lokaltog/vim-easymotion'
Bundle 'joequery/Stupid-EasyMotion.git'
Bundle 'rstacruz/sparkup', {'rtp': 'vim/'}
Bundle 'tpope/vim-rails.git'
Bundle 'kien/ctrlp.vim.git'
Bundle 'godlygeek/tabular.git'
Bundle 'scrooloose/syntastic.git'	
Bundle 'tpope/vim-surround.git'
Bundle 'flazz/vim-colorschemes.git'
Bundle 'klen/python-mode.git'
Bundle 'LaTeX-Box-Team/LaTeX-Box.git'
Bundle 'nelstrom/vim-markdown-folding.git'
Bundle 'bling/vim-airline'
Bundle 'jistr/vim-nerdtree-tabs'
Bundle 'octol/vim-cpp-enhanced-highlight'
Bundle 'terryma/vim-multiple-cursors.git'
Bundle 'vim-scripts/taglist.vim.git'
Bundle 'vim-scripts/L9.git'
Bundle 'nathanaelkane/vim-indent-guides.git'
Bundle 'Chiel92/vim-autoformat'
Bundle 'einars/js-beautify'
Bundle 'tpope/vim-unimpaired'
Bundle 'vim-scripts/Command-T.git'
Bundle 'tclem/vim-arduino.git'

" Snipmate bundle
Bundle "MarcWeber/vim-addon-mw-utils"
Bundle "tomtom/tlib_vim"
Bundle "garbas/vim-snipmate"
"Optional:
Bundle "honza/vim-snippets"

    
"=================================================================
"=================== Make Vim Nice ==============================
"=================================================================
"SetUp color-Scheme
set background=dark
colorscheme molokai 
"Add color column as a reference for coding
set colorcolumn=80
highlight ColorColumn ctermbg=233

hi Normal ctermbg=NONE

" Setting Up vim-indent-guides
let g:indent_guides_auto_colors = 1
"autocmd VimEnter,Colorscheme * :hi IndentGuidesOdd  guibg=red   ctermbg=3
"autocmd VimEnter,Colorscheme * :hi IndentGuidesEven guibg=green ctermbg=4
"Alternatively you can add the following lines to your colorscheme file.
hi IndentGuidesOdd  ctermbg=grey
hi IndkjdfentGuidesEven ctermbg=darkgrey

"GUI setup 
set toolbar=text,tooltips

"Setting Up line number
autocmd FocusLost   * : set number
autocmd InsertEnter * : set number
autocmd InsertLeave * : set relativenumber
autocmd CursorMoved * : set relativenumber

"Adding mapping and the default command to invoke CtrlP
let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd = 'CtrlP'


" Airline settings
set laststatus=2

" Syntastic C checker 
  "let g:loaded_syntastic_c_gcc_checker = 1 
  "let g:loaded_syntastic_c_splint_checker = 1


" Vim Multicursors Plugin SetUp
" Out of the box, only the single key Ctrl-n is mapped in regular
" Vim's Normal mode and Visual mode to provide the functionality
" mentioned above. Ctrl-n, Ctrl-p, Ctrl-x, and <Esc> are mapped
" in the special multicursor mode once you've added at least one
" virtual cursor to the buffer. If you don't like the plugin taking
" over your favorite key bindings, you can turn off the default with

let g:multi_cursor_use_default_mapping=0

"You can then map the 'next', 'previous', 'skip', and 'exit' keys like the following:

"Default mapping
"let g:multi_cursor_next_key='<c-m>'
"let g:multi_cursor_prev_key='<c-o>'
"let g:multi_cursor_skip_key='<c-i>'
"let g:multi_cursor_quit_key='<Esc>'

"By default, the 'next' key is also used to enter multicursor mode. If you
"want to use a different key to start multicursor mode than for selecting
"the next location, do like the following:
  
" Map start key separately from next key
"let g:multi_cursor_start_key='<F6>'


"Map Taglist to toggle the windows
nnoremap <C-l>        :TlistToggle<CR>

" Toggle spell checking on and off with `,s`
nmap <silent> <leader>s :set spell!<CR>
nmap <leader>p ]s
nmap <leader>o [s
"nmap <leader>m z=

" Arduino syntx highlight
au BufRead,BufNewFile *.pde set filetype=arduino
au BufRead,BufNewFile *.ino set filetype=arduino

" Snipmate keymap
imap <C-f> <Plug>snipMateNextOrTrigger
smap <C-f> <Plug>snipMateNextOrTrigger
	
"" YouCompleteMe
"let g:ycm_key_list_previous_completion=['<Up>']
let g:ycm_global_ycm_extra_conf = '~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp/ycm/.ycm_extra_conf.py'
