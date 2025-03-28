#!/bin/bash
# Install Typical use packages
sudo apt-get install --yes zsh git \
	emacs vim tmux ssh \
	build-essential checkinstall \
	cmake  cmake-curses-gui \
    golang \
	vifm \
	nmap \
	npm \
	htop pandoc \
	tree \
	ack-grep \
   	exuberant-ctags \
	xclip \
	powertop



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

# to install ranger from souce and have nice icons
# git clone https://github.com/ranger/ranger.git
# git clone https://github.com/alexanderjeurissen/ranger_devicons.git
# git clone https://github.com/ryanoasis/nerd-fonts.git
