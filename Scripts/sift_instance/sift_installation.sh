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
sudo sift install --mode=server
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get autoremove -y

#Install efs-utils to mount the EFS
sudo apt-get install -y git binutils make
mkdir /tmp/aws
cd /tmp/aws
git clone https://github.com/aws/efs-utils
cd efs-utils
make deb
sudo apt-get install -y ./build/amazon-efs-utils*deb

# Install required dependencies to install libaff4 

# dependencies - zlib
cd /opt
wget http://www.zlib.net/zlib-1.2.11.tar.gz
tar -xvzf zlib-1.2.11.tar.gz
cd zlib-1.2.11
./configure
make
make install

# dependencies - raptor2
sudo apt-get install libraptor2-dev -y

# dependencies -  google-glog
sudo apt-get install libgoogle-glog-dev libgoogle-glog0v5 libgoogle-glog-doc -y

# dependencies -  pcrexx
sudo apt-get install libpcre++-dev -y

# dependencies -  tclap (missing *.pc file - place in /opt/local/lib/pkgconfig/)
sudo apt-get install libtclap-dev -y

# dependencies - snappy
sudo apt-get install libsnappy-dev -y

# dependencies - uuid, gcc etc.
sudo apt-get install liburiparser-dev uuid-dev libspdlog-dev libgtest-dev cmake -y

#Install bison - http://ftp.gnu.org/gnu/bison/bison-3.5.tar.gz
cd /opt
wget http://ftp.gnu.org/gnu/bison/bison-3.5.tar.gz
cd /opt/bison-3.5
./configure
make
make install
ln -s /usr/local/bin/bison /usr/bin/bison

# Install google test
cd /opt
git clone https://github.com/google/googletest.git
cd /opt/googletest/googletest
cmake CMakeLists.txt
make
ln -s /opt/googletest/googletest/lib/*.a /usr/lib
ln -s include/gtest /usr/include

# Install AFF4
cd /opt
git clone https://github.com/google/aff4.git
cd /opt/aff4
./autogen.sh
make
make install