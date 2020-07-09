#Created on Wed Dec 25 12:47:44 2019
#@author: Amal Htait


#!/bin/sh

path=${PWD}
#echo "$path"


# if needed install those: python3, pip3, curl, npm
#ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
#brew install python3
#curl -O https://bootstrap.pypa.io/get-pip.py
#python3 get-pip.py
#brew install curl
#brew install node


# get the requirements
cd $path
pip3 install -r requirements.txt


# Get Elasticserach and Kibana
curl https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.5.1-darwin-x86_64.tar.gz --output elasticsearch.tar.gz
mkdir elasticsearch && tar -zxvf elasticsearch.tar.gz -C elasticsearch --strip-components 1
rm -r elasticsearch.tar.gz

curl https://artifacts.elastic.co/downloads/kibana/kibana-7.5.1-darwin-x86_64.tar.gz --output kibana.tar.gz
mkdir kibana && tar -zxvf kibana.tar.gz -C kibana --strip-components 1
rm -r kibana.tar.gz
