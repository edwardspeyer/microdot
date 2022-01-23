set clipboard=unnamed
set modeline

" Traditional colours
syntax on
set t_Co=8
"colorscheme hazkit

" Indenting magic
set autoindent
filetype indent on

" bufexplorer
map <C-J> :bprevious<cr>
map <C-K> :bnext<cr>
map <C-N> :bdelete<CR>
map <F5> :make<CR>

" Allow multiple buffers to be open
set hidden

" Highlight search matches
set hlsearch

" Make tab-autocompletion more bash-like
set wildmode=list:longest




"" vim: syntax=vim:et
"
"" Colors based on Ubuntu
"set t_Co=8
"syntax on
"colorscheme hazkit
"
"" Settings taken from the Debian defaults
"set nocompatible                " Use Vim defaults instead of 100% vi 
"                                " compatibility
"set backspace=indent,eol,start  " more powerful backspacing
"set autoindent                  " always set autoindenting on
"set textwidth=0                 " Don't wrap words by default
"set nobackup                    " Don't keep a backup file
"set viminfo='20,\"50            " read/write a .viminfo file, don't store more
"                                " than 50 lines of registers
"set history=50                  " keep 50 lines of command line history
"set ruler                       " show the cursor position all the time
"set showcmd                     " Show (partial) command in status line
"set showmatch                   " Show matching brackets
"set incsearch                   " Incremental search
"set autowrite                   " Automatically save before commands like :next
"                                " and :make
set modelines=24                " Allow modelines in the first `page'
"set noignorecase                " Override 'ignorecase' if it is on by default
"
"
"" My own settings that I like
"set hidden                       " Allow multiple buffers to be open
"set hlsearch                     " Highlight search matches
"set wildmode=list:longest        " Make tab-autocompletion more bash-like
"
"
"" Avoid the expitofdoom!
""
""   2008-01-16 12:40 <col> map Q <silent>
""   2008-01-16 12:40 <col> map gQ <silent>
""   2008-01-16 12:41 <col> aidehua: I think that should cover all the ways you
""                          might be getting into ex mode
""
"map Q  <silent>
"map gQ <silent>
"
"
"" Buffer fiddling shortcuts:
"map <C-J> :bprevious<cr>
"map <C-K> :bnext<cr>
"map <C-N> :bdelete<CR>
"map <F5> :make<CR>
"
"" Navigate the results of make-ing / grep-ing
""map <S-J> :cprevious<CR>
""map <S-K> :cnext<CR>
"
"" Recognise some extra file types:
"au BufNewFile,BufRead  svn-commit.* setf svn   " Subversion commits
"au BufNewFile,BufRead  *.qa,qa/*    setf yaml  " QA driver files
"au BufNewFile,BufRead  *.t          setf perl  " Perl unit tests
"au BufNewFile,BufRead  .labels,.info setf yaml " MusicStore files
"au BufNewFile,BufRead  *.rhtml      setf html  " ERB template files in RubyOnRails
"au BufNewFile,BufRead  ppp.conf     setf sh    " ppp config files look a bit like shell syntax :)
"au BufNewFile,BufRead  db.*         setf dns   " zonefiles
"
"
"" Expand tab by default, except for Makefiles!
set expandtab
:au Filetype make set noexpandtab
"
"" Settings for different file types:
:au Filetype xhtml,html,xml,xsl,xslt  set tabstop=2 shiftwidth=2
:au Filetype yaml               set tabstop=2 shiftwidth=2
:au Filetype ruby               set tabstop=2 shiftwidth=2
":au Filetype mail               set tabstop=2 shiftwidth=2 wrap textwidth=72
":au Filetype java               set tabstop=4 shiftwidth=4
":au Filetype apache             set tabstop=4 shiftwidth=4
:au Filetype sh                 set tabstop=2 shiftwidth=2
":au Filetype php                set tabstop=2 shiftwidth=2
:au Filetype python             set tabstop=4 shiftwidth=4 makeprg=autopep8\ -i\ %
:au Filetype javascript         set tabstop=2 shiftwidth=2
":au Filetype c                  set tabstop=4 shiftwidth=4
":au Filetype go                 set tabstop=8 shiftwidth=8
"
":au Filetype perl set makeprg=/usr/share/vim/vim63/tools/efm_perl.pl\ -c\ %\ $* 
"                    \ errorformat=%f:%l:%m
"                    \ tabstop=4
"                    \ shiftwidth=4
"
":au Filetype ruby set errorformat=\ \ \ \ %f:%l:%m,\	from\ %f:%l:%m,\	from\ %f:%l,%f:%l:%m
"
"" Set the grep program to ignore version controlled files
"set grepprg=grep\ -n\ $*\ /dev/null\ \\\|\ perl\ -lane\ 'print\ unless\ $F[0]\ =~\ m[/\.svn/]'
"
"" Turn on the mouse for console vim
""set mouse=a
"set mouse=n
"
"" Default Search colouring is bright-yellow on bright-white.  Great.  CHANGE
"" IT!  (...and other things.)
"highlight Search    ctermbg=Yellow ctermfg=DarkGray
"highlight VertSplit ctermbg=white  ctermfg=white term=NONE cterm=NONE
"
"" Make * a bullet point, not a comment prefix.
"set comments-=mb:*
"set comments+=fb:*
"
"" I pretty much *always* want a tabstop of 2 characters by default:
"set tabstop=2 shiftwidth=2
"
"" Needed to get vim 8 packages (like vim-go) to run their filedetect code
"filetype on
"filetype plugin on
"filetype indent on
"
"let g:go_fmt_command = "goimports"
"
"" OS X crontab editing
"au BufEnter /tmp/crontab.* setl backupcopy=yes
"
"set directory=$HOME/.vim/swapfiles
set noswapfile

" Middle mouse click to paste
"set clipboard=unnamed

" ^C / ^V clipboard
set clipboard=unnamedplus

:au Filetype markdown set formatoptions=rtq autoindent shiftwidth=2 tabstop=2 comments=f:*\ 

" Prettier splits
set fillchars+=vert:\┃
hi VertSplit ctermfg=Black ctermbg=Gray

:au Filetype css set tabstop=2 shiftwidth=2
