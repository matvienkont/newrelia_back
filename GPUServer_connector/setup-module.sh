#!/usr/bin/bash
apt install openssh-server
mkdir -p /drive/ngrok-ssh
cp sshd_config.txt /drive/ngrok-ssh
cd /drive/ngrok-ssh
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -O ngrok-stable-linux-amd64.zip
unzip -u ngrok-stable-linux-amd64.zip
cp /drive/ngrok-ssh/ngrok /ngrok
chmod +x /ngrok

cat sshd_config.txt > /drive/ngrok-ssh/sshd_config

pip3 install colab_ssh --upgrade

sudo apt-get install sshpass

mkdir -p /content/connection
touch /content/connection/GPU_server_connection_info
touch /content/connection/service_server_connection_info
