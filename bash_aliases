if [ -x /usr/bin/dircolors ]; then
# enable color support of ls and also add handy aliases
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    # export GREP_COLORS='0;32;42'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias hgp='history | grep --color=auto'
alias hcs="history | awk '{print \$2};' | sort | uniq -c | sort -rn | head -15"
alias findPCs='sudo nmap -sT 192.168.1.0/24'
alias connectDO='ssh root@178.62.204.199'


# Example aliases
alias zshconfig="vi ~/.zshrc"
alias ohmyzsh="vi ~/.oh-my-zsh"

#git tig aliases
#alias tig="git show | tig"
