#!/bin/bash
###############################################################################
#                   
# Docker installation script
#
###############################################################################
 uname -a
 sudo apt-get install apt-transport-https ca-certificates
 sudo apt-key adv \\n               --keyserver hkp://ha.pool.sks-keyservers.net:80 \\n               --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
 echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list
 cat /etc/apt/sources.list.d/docker.list
 sudo apt-get update
 apt-cache policy docker-engine

 sudo apt-get install linux-image-extra-$(uname -r)
 sudo apt-get install linux-image-extra-virtual
 sudo apt-get install docker-engine
 sudo apt-get update

 sudo service docker start
 sudo docker run hello-world

 sudo groupadd docker
 sudo usermod -aG docker $(whoami)

 #docker run -it ubuntu bash
 #sudo docker run -it ubuntu bash
 #sudo usermod -aG docker $USER
 #docker run hello-world
 #sudo reboot
