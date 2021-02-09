#!/bin/bash

# Script for installing necessary tools and packages for use of the Drink Machine application

# Check if this is being run as root
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Not running as root"
    exit
fi

echo "Installing apt packages"
apt-get update && apt-get install -y \
    wget \
    git \
    screen \
    vim \
    docker.io \
    docker-compose

echo "Docker setup..."
systemctl unmask docker.service
systemctl unmask docker.socket
systemctl start docker.service
systemctl enable docker

echo "Installing Node.js LTS"
curl -sL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
apt-get install -y nodejs

echo "Installing Angular"
npm install -g @angular/cli

echo "Finished."

