#Created on Wed Dec 25 12:47:44 2019
#@author: Amal Htait

#!/bin/sh

path=${PWD}

#echo "$path"

# if needed install those: python3, pip3, curl, npm
apt update
apt -y install python3
apt -y install python3-pip
apt -y install curl
apt -y install default-jre
apt -y install default-jdk
apt -y install npm

# get the requirements
cd $path
pip3 install -r requirements.txt


#Get elasticSearch and Kibana
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list
sudo apt update
sudo apt install elasticsearch
sudo apt install kibana
