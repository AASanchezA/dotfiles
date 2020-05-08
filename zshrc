# set %TERM for support 256 color bit 
[[ -n "$DISPLAY" && "$TERM" = "xterm" ]] && export TERM=xterm-256color  
# set a fancy prompt (non-color, unless we know we "want" color) 
case "$TERM" in 
	xterm-color) color_prompt=yes;; 
 	esac 

echo "Running ZSHRC, enjoy the day ¯\_(ツ)_/¯"

# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh 
 
# Disable flow control commands (keeps C-s from freezing everything) 
stty start undef 
stty stop undef 
	
# Alias definitions. 
# You may want to put all your additions into a separate file like 
# ~/.bash_aliases, instead of adding them here directly. 
# See /usr/share/doc/bash-doc/examples in the bash-doc package. 

if [ -f ~/.bash_aliases ]; then 
	. ~/.bash_aliases 
fi 
		  
# Export definitions. 
# You may want to put all your additions into a separate file like 
# ~/.bash_export, instead of adding them here directly. 
# See /usr/share/doc/bash-doc/examples in the bash-doc package. 

if [ -f ~/.bash_export ]; then 
	. ~/.bash_export 
fi

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
#ZSH_THEME="robbyrussell"
ZSH_THEME="blinks"
#ZSH_THEME="agnoster-newline"

# For Agnoster to Hide the Local User
DEFAULT_USER="andres"


# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git web-search systemadmin tmux ubuntu kubectl docker rsync gitignore minikube colored-man-pages)

source $ZSH/oh-my-zsh.sh

# User configuration
export PATH=$HOME/bin:/usr/local/bin:$PATH 
# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
if [[ -n $SSH_CONNECTION ]]; then
	export EDITOR='vim'
else
	export EDITOR='vim'
fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"
autoload -U edit-command-line
 #Vi style:
zle -N edit-command-line
bindkey -M vicmd v edit-command-line

# Disable matching
# unsetopt nomatch

# VIM mode 
vim() STTY=-ixon command vim "$@" 
bindkey -v 

bindkey '^P' up-history 
bindkey '^N' down-history 
bindkey '^?' backward-delete-char 
bindkey '^h' backward-delete-char 
bindkey '^w' backward-kill-word 
bindkey '^r' history-incremental-search-backward 
# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
alias zshconfig="vim ~/.zshrc"
alias ohmyzsh="vim ~/.oh-my-zsh"

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
