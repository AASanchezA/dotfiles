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
alias primusrunBlank="vblank_mode=0 primusrun"
alias findPCs='sudo nmap -sT 192.168.178.0/24'
alias findPrinters='nmap -p 9100,515,631 192.168.1.1/24'
alias connectDO='ssh andres@kurbis.combinado.cl'
alias connectDOAndres='ssh andres@kurbis.combinado.cl -i ~/.ssh/digitalOcean'

alias proxyPT='ssh -L 8888:127.0.0.1:8888 -p 2222 sato@brocoli.combinado.cl'
alias proxyDO='ssh -L 8888:127.0.0.1:8888 andres@178.62.204.199 -i ~/.ssh/digitalOcean'
alias proxyDO1='ssh -L 8888:127.0.0.1:8888 andres@178.62.207.97 -i ~/.ssh/digitalOcean'
alias proxyDO2='ssh -L 8888:127.0.0.1:8888 andres@kurbis.combinado.cl -i ~/.ssh/digitalOcean'
alias powerhtml='sudo powertop -r /var/www/power.html -t 60'

# Emacs aliases
alias e='emacs -nw'
alias ec='emacsclient'

# Vim Alias
alias v='vi'
alias vino='vi --noplugin'

# Example aliases
alias zshconfig="vi ~/.zshrc"
alias ohmyzsh="vi ~/.oh-my-zsh"

#git tig aliases
#alias tig="git show | tig"

# Cool Aliases for command that I always forget
alias useful='xdg-open http://www.pixelbeat.org/cmdline.html &'
alias listWireless='sudo iw dev wlp3s0 scan | grep SSID'
alias x='xdg-open'

alias diffme='git difftool --tool=vimdiff'

alias diskSpace='df -ah'
alias folderSize='du -sh'
alias openPorts='sudo netstat -tulpn'

## How to check services
# Old way
#service udev
#service udev status

# New way
#systemctl status udev
#systemctl status lightdm.service

# Check network drivers
#ifconfig
#ip
#ip addr show
