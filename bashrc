# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoredups:ignorespace

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

#this comand will set the bash input as VI mode
set -o vi
# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set %TERM for support 256 color bit
[[ -n "$DISPLAY" && "$TERM" = "xterm" ]] && export TERM=xterm-256color 
# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi

#Add Date to history
export HISTTIMEFORMAT="%h/%d - %H:%M:%S "
#Don't sava duplicate command
export HISTCONTROL=ignoreboth


alias android-connect="mtpfs -o allow_other /media/Galaxy"
alias android-disconnect="fusermount -u /media/Galaxy"

#insert cuda folder to the path
export PATH=/usr/local/cuda-5.0/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-5.0/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/local/cuda-5.0/lib64:$LD_LIBRARY_PATH

#Add IPP dependencies to the path
source /opt/intel/bin/compilervars.sh intel64
export LD_LIBRARY_PATH=/opt/intel/composer_xe_2013.5.192/ipp/lib/intel64/:$LD_LIBRARY_PATH

#Add Leap dependencies to the path
export LD_LIBRARY_PATH=/usr/lib/Leap/:$LD_LIBRARY_PATH

#add ros dependencies to path
#source /opt/ros/groovy/setup.bash

#Add wild magic dependencies
WM5_PATH=/usr/local/wild-magic-5.7 ; export WM5_PATH

#add texlive to the path
PATH=/usr/local/texlive/2013/bin/x86_64-linux:$PATH; export PATH

#add pcl 1.7 to the path
PATH=/usr/include/pcl-1.7:$PATH; export PATH

# sourcing git-completion
#\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h:\w\$
#export PS1='[\u@\h \W$(__git_ps1 " (%s)")]\$ '
#export PS1="\e[1;34m\u@\h \w> \e[m"
#export PS1='\[\e[1;34m\]\u@\h:\]\e[0m\]\[\e[1;31m\]$(__git_ps1 "(%s)")\[\e[0m\]\n\[\e[1;32m\]\w\a\[\e[0m\]\[\$\] '
export PS1='${debian_chroot:+($debian_chroot)}\[\e[1;34m\]\u@\h:\]\e[0m\]\[\e[1;31m\]$(__git_ps1 "(%s)")\[\e[0m\]\n\[\e[1;32m\]\w\a\[\e[0m\]\[\$\] '
source ~/.git-completion.sh
source ~/.git-prompt.sh

#ROS setup
#source /opt/ros/hydro/setup.bash


# added by Anaconda 1.9.2 installer
export PATH="/home/andres/anaconda/bin:$PATH"
