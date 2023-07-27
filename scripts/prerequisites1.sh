sudo apt update

#Install docker

sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable"
sudo apt update
apt-cache search docker-ce
sudo apt install docker-ce


#sudo systemctl status docker
sudo usermod -aG docker ${USER}
sudo passwd ubuntu
su - ${USER}
id -nG
