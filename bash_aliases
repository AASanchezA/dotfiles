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

function browse {
    # alias browse="xdg-open \$(git remote show origin |grep \"Fetch URL\" | awk -F': ' '{print \$2}')"
    URL=$(git remote get-url --all origin)
    echo "original $URL"
    if [[ $URL == git@* ]] 
    then
        URL=$(echo $URL | sed -e 's/\:/\//' -e 's/git@/https:\/\//')
    fi
    echo "opening $URL"
    xdg-open $URL
}

# move and copy
alias cp='cp -i'
alias mv='mv -i'

function ask_yes_or_no() {
    echo "Do you want to continue ([y]es or [N]o): "
    read REPLY
    case $(echo $REPLY | tr '[A-Z]' '[a-z]') in
        y|yes) return 0 ;;
        *)     return 1;;
    esac
}

# some more ls aliases
if command -v exa &> /dev/null
then
    alias ls='exa --git --icons'
fi

alias gut='git'
unalias gf
alias ll='ls -alF'
alias la='ls -a'
#alias l='ls -CF'
alias l='ls -aF'
alias lt='ls -FT'
alias hcs="history | awk '{print \$2};' | sort | uniq -c | sort -rn | head -15"
#alias glist='ghq list | fzf | xclip && cd "${GHQ_ROOT}/$(xclip -o)"'
alias plist="ghq list --full-path | fzf --preview \"bat --color always {}/README.md\" --preview-window=right,50%,nohidden"
alias glist="cd \$(ghq list --full-path| fzf --preview \"bat --color always {}/README.md\" --preview-window=right,50%,hidden --bind='?:toggle-preview')"
#alias glist="cd $HOME/Proj/\$(ghq list | fzf --preview \"bat --color always $HOME/Proj/{}/README.md\" --preview-window=right,50%,nohidden)"
alias tde='glist && ide'
alias findPCs="sudo nmap -sT \$(ip -brief address |grep UP|grep -e wl -e enp |awk '{print \$3};' | head -1| sed -e 's/.[0-9]\+\/24$/.0\/24/')"
alias findPrinters="nmap -p 9100,515,631 \$(ip -br a |grep UP|grep -e wl -e enp |awk '{print \$3}' | head -1| sed -e 's/.[0-9]\+\/24$/.0\/24/') -oG - | grep \\/open |awk '{print \$2\"->\"\$3}'"


alias powerhtml='sudo powertop -r /var/www/power.html -t 60'
alias loadKey='eval "$(ssh-agent)" && ssh-add ~/.ssh/id_rsa'

# fzf utils
# TODO put a check before killing the process
alias killme="ps aux |fzf | awk '{print \$2}' |xargs -I{} kill {}"
alias killit="ps aux |fzf | awk '{print \$2}' |xargs -I{} kill -s KILL {}"
alias deleteme="ls --reverse --sort=size -l |fzf | awk '{print \$7}' | xargs -n1 -I{} rm -vf {}"
alias tldd="tldr --list | sed -e 's/,/\n/g' -e \"s/'//g\" -e 's/\[//g' -e 's/\]//g' | fzf --preview \"tldr {1} --color\" --preview-window=right,70%,nohidden | xargs tldr"
alias cleansnap="snap list --all | awk '/disabled/{print \$1, \$3}' | while read snapname revision; do sudo snap remove \$snapname --revision=\$revision; done"

# cat to bat
if command -v bat &> /dev/null
then
    alias cat='bat --theme=base16'
fi

# Emacs aliases
#alias emacs='/home/andres/tools/bin/emacs'
#alias emacsclient='/home/andres/tools/bin/emacsclient'
alias e='emacs -nw'
alias eg='emacsclient -create-frame --alternate-editor=""' 
alias ec='emacsclient --alternate-editor="" -t'

# Vim Alias
alias v='vim'
if command -v nvim &> /dev/null
then
    alias v='nvim'
fi
alias V='sudo --preserve-env nvim'
alias vino='v --noplugin'
alias f='v -u ~/.fastvimrc'
alias vf='v $(fzf --height 40%)'
alias ef='e $(fzf --height 40%)'

# Ranger Alias
if command -v ranger &> /dev/null
then
    alias ra="ranger"
fi

# Example aliases
alias zshconfig="vi ~/.zshrc"
alias ohmyzsh="vi ~/.oh-my-zsh"

# Cool Aliases for command that I always forget
alias useful='xdg-open http://www.pixelbeat.org/cmdline.html &'
alias listWireless='sudo iw dev wlp3s0 scan | grep SSID'
alias x='xdg-open'

# Some git aliases
alias diffme='git difftool --tool=vimdiff'
alias diffchanges='git diff @{1}..'
alias gitLOC='git ls-files -z  | xargs -0 cat | wc -l'

# useful stuff
alias diskSpace='df -ah'
alias folderSize='du -sh'
alias openPorts='sudo netstat -tulpn'

# New way
#systemctl status udev
#systemctl status lightdm.service

# Check network drivers
#ifconfig
#ip
#ip addr show
# Postman not output to console
alias Postman='~/bin/Postman </dev/null &>/dev/null &'
# find proccess
alias got='ps fax |fzf'
alias clipme='xclip -selection clip'
alias hungry='ps -e -o pcpu,cpu,nice,state,cputime,args --sort pcpu  |sort --reverse |head'

plotme()
{
    history -E | awk -F' [0-9]+:[0-9]+  ' '{print $1}' | awk '{print $2}' | uniq -c | gnuplot -p  -e 'set boxwidth 0.5; plot "-" using 1:xtic(2) with boxes'
}

# unalias gf
weather()
{
    local request="wttr.in/${1-Munich}"
    [ "$(tput cols)" -lt 125 ] && request+='?n'
    curl -H "Accept-Language: ${LANG%_*}" --compressed "$request"
}

memtop()
# List top consumer of memory on the system
{
{
	echo "_PID_ _Name_ _Mem_"
	for i in /proc/[0-9]*
		do
			echo -e "${i##*/}\t$(<$i/comm)\t$(pmap -d "${i##*/}" |\
				tail -1 | {
				read a b c mem d
			    echo $mem
			}
		)"
		done |\
			sort -nr -k3 |\
			head -$((${LINES:-23} - 5))
		} |\
column -t
} 2>/dev/null

debug_ssl_certificates()
{
    echo "checking {$1}"
    curl --insecure -vvI "https://{$1}" 2>&1 | awk 'BEGIN { cert=0 } /^\* SSL connection/ { cert=1 } /^\*/ { if (cert) print }'
    ask_yes_or_no
    if [ "$?" -eq "0" ]; then
       openssl s_client -connect "$1":443 </dev/null 2>/dev/null | openssl x509 -inform pem -text
    fi
    echo "Done"
}

alias siemens_chrome_proxy='nice -n 10 google-chrome-stable --user-data-dir="${HOME}/chrome_crap/todelete"  --proxy-server="https=127.0.0.1:9999;http=127.0.0.1:9999"'
alias siemens_chrome='nice -n 10 google-chrome-stable --user-data-dir="${HOME}/chrome_crap/todelete"'

function move_to_center() {
    eval "$(xdotool getactivewindow getwindowgeometry --shell)"
    t_x=$(tmux display -p '#{cursor_y}')
    t_y=$(tmux display -p '#{cursor_x}')
    notify-send --app-name="DUMMY" "HERE I AM in tmux $t_y $t_x and globaly $WIDH $HEIGHT $WINDOW"
    mov_y=$((HEIGHT / 2))
    mov_x=$((WIDTH / 2))
    xdotool mousemove --window "$WINDOW" $mov_x $mov_y
}

function lookfor () {
    argc=$(echo "$@" | wc -w)
    if [[ $argc -gt 1 ]]; then
          echo "Error: Invalid argument" "$@" "only support ONE arg!" >&2
          return 1
    fi
    lookForPackage="$1"
    paru -Ss "$lookForPackage" | fzf | xargs -I{} echo paru -S {} || echo "Nothing to do"

}
