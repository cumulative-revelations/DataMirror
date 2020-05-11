#Created on Wed Dec 25 12:47:44 2019
#@author: Amal Htait

#!/bin/sh

path=${PWD}

# run elasticsearch ( delete its content when testing )
echo "run elasticsearch"
sudo systemctl stop elasticsearch
sudo systemctl start elasticsearch 
sudo systemctl enable elasticsearch

sleep 10s


echo "delete all from elasticsearch"
curl -XDELETE localhost:9200/*
sleep 5s


#Fix Data files and Insert Indexes into elasticsearch
echo "run main"
#cd $path/script
python3 script/transformer/main.py


# run kibana then delete its content
echo "run kibana"
sudo systemctl stop kibana
sudo systemctl enable kibana
sudo systemctl start kibana 
sleep 30s

echo "run Vega Server"
gnome-terminal -- bash -c "npm install http-server -g; http-server '$path'/vegaFiles -p 8080 --cors; exec bash"
	

# run kibana then insert stuff
cd ..
curl -X POST "localhost:5601/api/saved_objects/_import" -H "kbn-xsrf: true" --form file=@$path/toImport/IndexPatterns_Visualisations.ndjson



#Open kibana
sensible-browser http://localhost:5601/app/kibana\#/dashboards\?\_g\=\(\)


