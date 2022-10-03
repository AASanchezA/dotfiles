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

" Use Vim settings, rather than Vi settings (much better!).
" This must be first, because it changes other options as a side effect.
set nocompatible


set path+=**
set wildmenu

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
set completeopt=menu,menuone,noselect

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
"set expandtab
set copyindent
set preserveindent
set shiftwidth=4
set softtabstop=0
set shiftwidth=4
set tabstop=4
set listchars=eol:¬,tab:>·,trail:~,extends:>,precedes:<,space:.

"=================================================================
"=================== Setting Up temp file ========================
"=================================================================
" controls where backup files (with ~ extension by default) go.
set backupdir=~/.vim/vimtmp

" The 'directory' option controls where swap files go.
set directory=~/.vim/vimtmp

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

"=================================================================
"=================== Useful Keybindings ==========================
"=================================================================
"This unsets the "last search pattern" register by hitting return
nnoremap <CR><CR> :noh<CR><CR>

"remap to save file with ctr+s
inoremap <C-s> <esc>:w<cr>
nnoremap <C-s> :w<cr>
"inoremap <C-S> <esc>:w !sudo tee %<cr>
"nnoremap <C-S> :w !sudo tee %<cr>
nnoremap <C-d> <C-d>zz
nnoremap <C-u> <C-u>zz

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
"map <C-f> g4 

" remaping square brackets
"nnoremap ü <]>
"nnoremap Ü <[>

" Easier moving of code Blocks
" better indetation
vnoremap < <gv 
vnoremap > >gv

" easier moving between tabs
map <Leader><leader>n <esc>:tabprevious<CR>
map <Leader><leader>m <esc>:tabnext<CR>


"=================================================================
"=================== Vundle Packages Manager ===================
"=================================================================

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
call vundle#begin()

" let Vundle manage Vundlewurden gerne dabei sein
" required! 
Bundle 'gmarik/vundle'

"=================================================================
"=================== My Vim Plugins ==============================
"=================================================================
" My Bundles here:
"original repos on github
Bundle 'preservim/nerdtree'

Bundle 'scrooloose/nerdcommenter'
"Bundle 'scrooloose/syntastic.git'	
"Bundle 'dense-analysis/ale'
"Bundle 'Valloric/YouCompleteMe.git'

Bundle 'bling/vim-airline'
Bundle 'tpope/vim-fugitive'

Bundle 'vim-scripts/taglist.vim.git'
"Bundle 'vim-scripts/L9.git'
Bundle 'rstacruz/sparkup', {'rtp': 'vim/'}

Bundle 'tpope/vim-surround.git'
Bundle 'tpope/vim-unimpaired'
Bundle 'flazz/vim-colorschemes.git'

Bundle 'klen/python-mode.git'

Bundle 'LaTeX-Box-Team/LaTeX-Box.git'
Bundle 'nelstrom/vim-markdown-folding.git'

Bundle 'nathanaelkane/vim-indent-guides.git'
Bundle 'Chiel92/vim-autoformat'
Bundle 'einars/js-beautify'

Bundle 'fatih/vim-go'

Bundle 'dyng/ctrlsf.vim'
Bundle 'sheerun/vim-polyglot'

Bundle 'junegunn/fzf', { 'dir': '~/tools/fzf', 'do': './install --all' }
Bundle 'junegunn/fzf.vim'


" Google vim script
"Bundle 'google/vim-glaive'
"Bundle 'google/vim-codefmt'
"Bundle 'google/vim-maktaba'
"Bundle 'google/vim-searchindex'

if has('nvim')
  " test
  Bundle 'nvim-lua/plenary.nvim'
  Bundle 'nvim-telescope/telescope.nvim'
  Bundle 'glacambre/firenvim', { 'do': { _ -> firenvim#install(0) } }
  Bundle 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
  Bundle 'neovim/nvim-lspconfig'

  "" setting up nvim-cmp
  Bundle 'hrsh7th/nvim-cmp'
  Bundle 'hrsh7th/cmp-buffer'
  Bundle 'hrsh7th/cmp-path'
  Bundle 'hrsh7th/cmp-nvim-lua'
  Bundle 'hrsh7th/cmp-nvim-lsp'
  "Bundle 'saafparwaiz1/cmp_luasnip'
endif

" TODO try if useful
"Bundle 'google/vim-syncopate'


" Snipmate bundle
"Bundle "MarcWeber/vim-addon-mw-utils"
"Bundle "tomtom/tlib_vim"
Bundle "SirVer/ultisnips"
Bundle "quangnguyen30192/cmp-nvim-ultisnips"
"Bundle "garbas/vim-snipmate"
"Optional:
"Bundle "honza/vim-snippets"

"Bundle "wakatime/vim-wakatime"
Bundle "ryanoasis/vim-devicons"

call vundle#end()

"=================================================================
"=================== Make Vim Nice ==============================
"=================================================================
"SetUp color-Scheme
set background=dark
colorscheme gruvbox
"Add color column as a reference for coding
set colorcolumn=80
highlight ColorColumn ctermbg=233

hi Normal ctermbg=NONE

"Alternatively you can add the following lines to your colorscheme file.
hi IndentGuidesOdd  ctermbg=grey
hi IndkjdfentGuidesEven ctermbg=darkgrey

"GUI setup re-enable for gvim
"set toolbar=text,tooltips

"Setting Up line number
autocmd FocusLost   * : set number
autocmd InsertEnter * : set number
autocmd InsertLeave * : set relativenumber
autocmd CursorMoved * : set relativenumber

"=================================================================
"=================== NerdTree Settings ===========================
"=================================================================
"How can I open a NERDTree automatically when vim starts up?
"autocmd vimenter * NERDTree

"How can I open a NERDTree automatically when vim starts up if no files were specified?
"autocmd vimenter * if !argc() | NERDTree | endif

"How can I close vim if the only window left open is a NERDTree?
"autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTreeType") && b:NERDTreeType == "primary") | q | endif

"=================================================================
"=================== Plugins Settings ============================
"=================================================================
" Setting Up vim-indent-guides
let g:indent_guides_auto_colors = 1
"autocmd VimEnter,Colorscheme * :hi IndentGuidesOdd  guibg=red   ctermbg=3
"autocmd VimEnter,Colorscheme * :hi IndentGuidesEven guibg=green ctermbg=4

" Airline settings
set laststatus=2
" youcomplete keybinding
"nmap <leader>gg :YcmCompleter GoTo<CR>
"nmap <leader>gh :YcmCompleter GetDoc<CR>
"nmap <leader>gf :YcmCompleter Format<CR>
"nmap <leader>gi :YcmCompleter GoToInclude<CR>
"nmap <leader>gd :YcmCompleter GoToDefinition<CR>
"nmap <leader>gr :YcmCompleter GoToReferences<CR>

"fast togle between last/current buffer
nnoremap <space><tab>  <C-^> 
" Buffers - explore/next/previous: 
nnoremap <leader>n   :bn<CR>
nnoremap <leader>m   :bp<CR>
" Buffers - explore/next/previous: 

" FZF keybindings
nmap <c-p> :Files<CR>
nnoremap <leader>fs :GFiles?<CR>
nnoremap <leader>pf :GFiles<CR>
nnoremap <space>ff :Files /<CR>
nnoremap <leader>fh :History<CR>
nnoremap <leader>fr :Rg<CR>
nnoremap <leader>fl :Lines<CR>
nnoremap <space>bb :Buffers<CR>
nnoremap <leader>hh :Helptags<CR>

" Nerdtree
map <C-n> :NERDTreeToggle<CR>

" Syntastic C checker 
  "let g:loaded_syntastic_c_gcc_checker = 1 
  "let g:loaded_syntastic_c_splint_checker = 1
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

" Firevim settings
au BufEnter github.com_*.txt set filetype=markdown
au BufEnter code.siemens.com_*.txt set filetype=markdown
au BufEnter gitlab.com_*.txt set filetype=markdown
au BufEnter outlook.office.com_*.txt set filetype=txt
au BufEnter yammer.com_*.txt set filetype=markdow


" Snipmate keymap
"imap <C-f> <Plug>snipMateNextOrTrigger
"smap <C-f> <Plug>snipMateNextOrTrigger
	
"" Latex-Box
"let g:LatexBox_latexmk_options = '-pdflatex="lualatex"'

" Trigger configuration. Do not use <tab> if you use
"  https://github.com/Valloric/YouCompleteMe.
"let g:UltiSnipsExpandTrigger="<c-t>"
"let g:UltiSnipsJumpForwardTrigger="<c-b>"
"let g:UltiSnipsJumpBackwardTrigger="<c-z>"

" If you want :UltiSnipsEdit to split your window.
"let g:UltiSnipsEditSplit="vertical"

" Add helloworld to the runtime path. (Normally this would be done with
" another
" Plugin command, but helloworld doesn't have a repository of its own.)
"call maktaba#plugin#Install(maktaba#path#Join([maktaba#Maktaba().location,
    "\ 'examples', 'helloworld']))

" the glaive#Install() should go after the "call vundle#end()"
"call glaive#Install()

" Optional: Enable codefmt's default mappings on the <Leader>= prefix.
"Glaive codefmt plugin[mappings]

" Configure helloworld using glaive.
"Glaive helloworld plugin[mappings] name='Bram'

"Glaive codefmt google_java_executable='java -jar /path/to/google-java-format.jar'
" Real world example: configure vim-codefmt
