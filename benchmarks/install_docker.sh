sudo yum install -y yum-utils
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo -y
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
systemctl start docker
