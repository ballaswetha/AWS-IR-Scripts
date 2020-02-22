sudo su <<HERE
set -e
echo "Started"
sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) main universe restricted multiverse"
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install git locales locales-all -y

#Install efs-utils to mount the EFS
sudo apt-get install -y git binutils make
cd /opt
git clone https://github.com/aws/efs-utils
cd /opt/efs-utils
make deb
sudo apt-get install -y ./build/amazon-efs-utils*deb

mkdir -p $sift_home
cd $sift_home
curl --silent  -Lo $sift_home/sift-cli-linux.sha256.asc https://github.com/teamdfir/sift-cli/releases/download/v1.8.0/sift-cli-linux.sha256.asc
curl --silent -Lo $sift_home/sift-cli-linux https://github.com/sans-dfir/sift-cli/releases/download/v1.8.0/sift-cli-linux
gpg --keyserver hkp://pool.sks-keyservers.net:80 --recv-keys 22598A94
gpg --verify $sift_home/sift-cli-linux.sha256.asc
sha256sum -c $sift_home/sift-cli-linux.sha256.asc
mv $sift_home/sift-cli-linux /usr/bin/sift
chmod 755 /usr/bin/sift
sift install --mode=server
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get autoremove -y

HERE
