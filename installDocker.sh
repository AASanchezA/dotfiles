#!/usr/bin/env bash

# Install Docker in Siemens Enviroment, With Proxy setup and so...

# Installation https://docs.docker.com/install/linux/docker-ce/ubuntu/
# Proxy Setup https://stackoverflow.com/questions/26550360/docker-ubuntu-behind-proxy

echo "Prepare dependencies"
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo docker run hello-world

echo "Setting app Proxy"
sudo mkdir /etc/systemd/system/docker.service.d
http_proxy_file=/etc/systemd/system/docker.service.d/http-proxy.conf
sudo echo "[service]" >> $http_proxy_file
sudo echo "environment=\"http_proxy=${http_proxy}/\"" >> $http_proxy_file
sudo echo "environment=\"https_proxy=${http_proxy}/\"" >> $http_proxy_file
sudo echo "environment=\"no_proxy=${NO_PROXY}\"" >> $http_proxy_file


# setup daemon.
cat > /etc/docker/daemon.json <<EOF
{
"exec-opts": ["native.cgroupdriver=systemd"],
"log-driver": "json-file",
"log-opts": {
"max-size": "100m"
},
"storage-driver": "overlay2"
}
EOF
mkdir -p /etc/systemd/system/docker.service.d


echo "Restart docker daemon"
sudo systemctl daemon-reload
sudo systemctl restart docker

echo "Add User to docker group"
sudo groupadd docker
sudo usermod -aG docker $USER
# sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
docker run hello-world
echo "\n\nDont Forget to logoff and login"


echo "Install Docker Compose"
curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o $HOME/tools/bin/docker-compose

chmod +x $HOME/tools/bin/docker-compose
