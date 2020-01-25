#! /bin/bash

#Reference - https://github.com/teamdfir/sift-cli

cd /home/ubuntu
mkdir sift
cd sift
wget https://github.com/teamdfir/sift-cli/releases/download/v1.8.0/sift-cli-linux.sha256.asc
wget https://github.com/teamdfir/sift-cli/releases/download/v1.8.0/sift-cli-linux
# ln -s /usr/bin/sha1sum /usr/bin/shasum (Depends on whether or sha256sum is available)
gpg --keyserver hkp://pool.sks-keyservers.net:80 --recv-keys 22598A94
gpg --verify sift-cli-linux.sha256.asc
sha256sum -c sift-cli-linux.sha256.asc
sudo mv sift-cli-linux /usr/bin/sift
chmod 755 /usr/bin/sift
sudo sift install
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get autoremove -y

#Install efs-utils to mount the EFS
sudo apt-get install -y git binutils make
mkdir /tmp/aws
cd /tmp/aws
git clone https://github.com/aws/efs-utils
cd efs-utils
make deb
sudo apt-get install -y ./build/amazon-efs-utils*deb
