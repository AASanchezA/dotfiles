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
	htop pandoc \
	tree \
	ruby-full \


# For Nodejs you need to do some changes
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
#sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}

# add in ~/.profile
# export PATH=~/.npm-global/bin:$PATH
# source ~/.profile
# To Update nodejs using npm
#sudo npm cache clean -f
#sudo npm install -g n
#sudo n stable

