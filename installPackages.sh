#!/bin/bash
# Install Typical use packages
sudo apt-get install zsh git \
	emacs vim tmux ssh \
	python python-pip ipython \
	build-essential checkinstall \
   	ctags \
	cmake cmake-qt-gui \
	nmap zenmap \
	npm \


# For Nodejs you need to do some changes
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'

# To Update nodejs using npm
#sudo npm cache clean -f
#sudo npm install -g n
#sudo n stable

