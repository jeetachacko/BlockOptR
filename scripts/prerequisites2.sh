sudo apt update

#Install docker compose

sudo curl -L https://github.com/docker/compose/releases/download/1.28.5/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

#Install Go

curl -O https://storage.googleapis.com/golang/go1.19.linux-amd64.tar.gz
sha256sum go1.19.linux-amd64.tar.gz
tar -xvf go1.19.linux-amd64.tar.gz
sudo mv go /usr/local

echo "export GOPATH=$HOME/go" >> ~/.profile
echo "export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin" >> ~/.profile
echo "export GOPATH=$HOME/go" >> ~/.bashrc
echo "export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin" >> ~/.bashrc

source ~/.bashrc
source ~/.profile

sudo apt-get update
sudo apt-get install build-essential openssl libssl-dev pkg-config

sudo apt-get install jq

sudo apt install python3-pip
pip3 install numpy
pip3 install arrow


#Install nvm

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
source ~/.bashrc

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion


nvm list-remote
nvm install v18.16.0
nvm list
nvm use v18.16.0

mkdir log_extraction/data

#install fabric samples
curl -sSL https://bit.ly/2ysbOFE | bash -s

npm i fabric-client

npm install --only=prod @hyperledger/caliper-cli@0.5.0
npx caliper bind --caliper-bind-sut fabric:2.2
