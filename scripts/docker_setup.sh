#Use docker without sudo
sudo usermod -aG docker ${USER}
sudo passwd ubuntu
su - ${USER}
id -nG
