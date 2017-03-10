#!/bin/bash
sudo apt-get update
sudo apt-get install tmux
sudo apt install yum
sudo apt install python-pip
pip install --upgrade pip
sudo apt install upstart
sudo apt-get install upstart-sysv
sudo update-initramfs -u
sudo apt-get install build-essential libyaml-dev libfftw3-dev libavcodec-dev libavformat-dev libavutil-dev libavresample-dev python-dev libsamplerate0-dev libtag1-dev libsodium-dev
sudo apt-get install python-numpy-dev python-numpy python-yaml
git clone https://github.com/MTG/essentia.git
chdir /home/ubuntu/essentia/
./waf configure --mode=release --build-static --with-python --with-cpptests --with-examples --with-vamp
./waf
sudo ./waf install
sudo apt install ipython
sudo apt-get install python-psycopg2
sudo apt-get install python-matplotlib
sudo pip install requests
sudo pip install rauth
sudo pip install seaborn
sudo pip install pymongo
sudo apt install mutt
sudo apt install postfix
sudo pip install jupyter
sudo apt install awscli
sudo apt-get install postgresql postgresql-contrib
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
sudo apt-get install -y mongodb
chdir /home/ubuntu/
git clone https://github.com/silkaitis/new_release_prediction.git
