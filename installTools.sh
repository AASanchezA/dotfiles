#!/usr/bin/env bash

mkdir ~/tools



# Install Ranger


# Install fzf
git clone https://github.com/junegunn/fzf.git --depth 1
# Install Rush and fd
curl https://sh.rustup.rs -sSf | sh
cargo install fd-find

#Install Ranger
git clone https://github.com/alexanderjeurissen/ranger_devicons.git --depth 1
git clone https://github.com/ryanoasis/nerd-fonts.git --depth 1
git clone https://github.com/ranger/ranger.git --depth 1

#Install Anaconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
