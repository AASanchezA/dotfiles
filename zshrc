# PROFILE Uncomment follow line and line at the bottom of the file to enable zprof profiler
# zmodload zsh/zprof

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
	
# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="robbyrussell"
# ZSH_THEME="spaceship"
# ZSH_THEME="passion"
# ZSH_THEME="blinks"
#ZSH_THEME="agnoster-newline"

# For Agnoster to Hide the Local User
DEFAULT_USER="andres"

# TODO check for speedup loading
# SPACESHIP_PROMPT_ORDER=(user host dir git exec_time line_sep jobs exit_code char)

# SPACESHIP settings
SPACESHIP_VI_MODE_SHOW="false"
SPACESHIP_EXIT_CODE_SHOW="true"
SPACESHIP_EXEC_TIME_SHOW="true"
SPACESHIP_EXEC_TIME_ELAPSED="1"
SPACESHIP_JOBS_SHOW="true"

# SPACESHIPT LANGUAGE
SPACESHIP_GOLANG_SHOW="false"
SPACESHIP_NODE_SHOW="false"
SPACESHIP_PACKAGE_SHOW="false"
SPACESHIP_RUST_SHOW="false"
SPACESHIP_HASKELL_SHOW="false"
SPACESHIP_RUBY_SHOW="false"
SPACESHIP_AWS_SHOW="false"
SPACESHIP_GCLOUD_SHOW="false"
SPACESHIP_KUBECTL_SHOW="false"
SPACESHIP_TERRAFORM_SHOW="false"
SPACESHIP_DOCKER_SHOW="false"
SPACESHIP_DOCKER_CONTEXT_SHOW="false"
SPACESHIP_PHP_SHOW="false"
SPACESHIP_XCODE_SHOW="false"
SPACESHIP_SWIFT_SHOW="false"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
DISABLE_AUTO_UPDATE="true"

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

# History size
HISTSIZE=100000
# Save history after logout
SAVEHIST=100000

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
  zsh-autosuggestions
  git
  web-search
  systemadmin
  tmux
  # ubuntu
  # kubectl
  docker
  docker-compose
  rsync
  gitignore
  #minikube
  fd
  ripgrep
  colored-man-pages
  nmap
  pass
)

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
bindkey '^ ' autosuggest-accept
# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
alias zshconfig="vim ~/.zshrc"
alias ohmyzsh="vim ~/.oh-my-zsh"

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

test $(command -v fzf) && eval "$(fzf --zsh)" || echo "Fzf not installed"
test $(command -v fd) && true || echo "Please Install fd"

# Exclude those directories even if not listed in .gitignore, or if .gitignore is missing
FD_OPTIONS="--follow --exclude .git --exclude node_modules"

test $(command -v gf) && source $GOPATH/pkg/mod/github.com/tomnomnom/gf@v0.0.0-20200618134122-dcd4c361f9f5/gf-completion.zsh || echo "Please Install gf from https://github.com/tomnomnom/gf"

# Change behavior of fzf dialogue
export FZF_DEFAULT_OPTS="--no-mouse --height 20% -1 --reverse --multi --inline-info --preview='[[ \$(file --mime {}) =~ binary ]] && echo {} is a binary file || (bat --style=numbers --color=always {} || cat {}) 2> /dev/null | head -300' --preview-window='right:hidden:wrap' --bind='f3:execute(bat --style=numbers {} || less -f {}),f2:toggle-preview,ctrl-d:half-page-down,ctrl-u:half-page-up,ctrl-a:select-all+accept,ctrl-y:execute-silent(echo {+} | pbcopy)'"

# Change find backend
# Use 'git ls-files' when inside GIT repo, or fd otherwise
export FZF_DEFAULT_COMMAND="git ls-files --cached --others --exclude-standard | fd --type f --type l $FD_OPTIONS"

# Find commands for "Ctrl+T" and "Opt+C" shortcuts
export FZF_CTRL_T_COMMAND="fd . $FD_OPTIONS"
export FZF_ALT_C_COMMAND="fd --type d $FD_OPTIONS"
export FZF_ALT_C_OPTS="--preview 'exa --tree --color=always {} | head -200'"
export FZF_CTRL_R_OPTS="--preview 'echo {}' --preview-window down:3:hidden:wrap --bind '?:toggle-preview' --bind 'ctrl-y:execute-silent(echo -n {2..} | xclip -selection clipboard; sleep 0.35s)+abort' --header 'Press CTRL-Y to copy command into clipboard'"

# Advanced customization of fzf options via _fzf_comprun function
# - The first argument to the function is the name of the command.
# - You should make sure to pass the rest of the arguments to fzf.
_fzf_comprun() {
  local command=$1
  shift

  case "$command" in
    cd)           fzf --preview 'exa --tree --color=always {} | head -200' "$@" ;;
    export|unset) fzf --preview "eval 'echo \$'{}"         "$@" ;;
    ssh)          fzf --preview 'dig {}'                   "$@" ;;
    *)            fzf --preview "bat -n --color=always --line-range :500 {}" "$@" ;;
  esac
}

export ZSH_AUTOSUGGEST_STRATEGY=(history completion)
export ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=#858821,bg=#002B36,bold"
#export ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=#3A3A3A,bold,standout"




# Load Angular CLI autocompletion.
test $(command -v ng) && source <(ng completion script) || echo "ng not installed"

[ -f /opt/mambaforge/etc/profile.d/conda.sh ] && source /opt/mambaforge/etc/profile.d/conda.sh

# PROFILE Uncomment follow line and line at the top of the file to enable zprof profiler
# zprof
