#!/bin/bash
############################
# .make.sh
# This script creates symlinks from the home directory to any desired dotfiles in ~/dotfiles
############################

########## Variables

dir=~/dotfiles                    # dotfiles directory
olddir=~/dotfiles_old             # old dotfiles backup directory
files="vimrc fastvimrc vim zshrc oh-my-zsh tmux.conf"    # list of files/folders to symlink in homedir

##########

# create dotfiles_old in homedir
echo "Creating $olddir for backup of any existing dotfiles in ~"
mkdir -p $olddir
echo "...done"

# change to the dotfiles directory
echo "Changing to the $dir directory"
cd $dir
echo "...done"

# move any existing dotfiles in homedir to dotfiles_old directory, then create symlinks 
for file in $files; do
	echo "Moving any existing dotfiles from ~ to $olddir"
	mv ~/.$file ~/dotfiles_old/
	echo "Creating symlink to $file in home directory."
	ln -s $dir/$file ~/.$file
done

# linking also bash alias file
echo "Creating symlink to bash_aliases in home directory."
ln -s $dir/bash_aliases ~/.bash_aliases
cp $dir/bash_export ~/.bash_export

# linking Spacemacs config
echo "Creating symlink to Spacemacs folder and configuration file"
ln -s $dir/spacemacs ~/.emacs.d
ln -s $dir/spacemacsrc ~/.spacemacs

if ! [ -d ~/.config ]; then mkdir ~/.config; fi

echo "Creating symlink to nvim folder"
ln -s $dir/nvim ~/.config/nvim

echo "Creating symlink to vifm folder"
ln -s $dir/config/vifm ~/.config/vifm

echo "Create temp folder in vim dir"
mkdir $dir/vim/vimtmp

# Define Zsh, as my default Shell
#sudo chsh -s /bin/zsh

echo "Creating symlink for Reveal.js in opt folder"
#ln -s $dir/reveal.js /opt/reveal.js

echo "Creating symlink to oh-my-zsh autosuggestion folder"
ln -s $dir/zsh-autosuggestions $dir/oh-my-zsh/custom/plugins/zsh-autosuggestions

echo "Creating symlink to local scripts folder"
ln -s $dir/scripts ~/bin
