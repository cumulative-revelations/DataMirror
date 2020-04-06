#Created on Wed Dec 25 12:47:44 2019
#@author: Amal Htait


#!/bin/sh

path=${PWD}
#echo "$path"

# get the zipped files (as many as I need ? )
#python3 upload_zippedFile.py $path/script/dataSource


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

# run elasticsearch ( delete its content when testing )
echo "run elasticsearch"
osascript -e 'tell app "Terminal"
    do script "cd '$path'/elasticsearch; bin/elasticsearch"
end tell'

sleep 30s

#echo "delete all from elasticsearch"
curl -XDELETE localhost:9200/*
sleep 5s


#Fix Data files and Insert Indexes into elasticsearch
echo "run main"
#cd $path/script
python3 script/transformer/main.py


# run kibana then delete its content
echo "run kibana"
osascript -e 'tell app "Terminal"
    do script "cd '$path'/kibana;bin/kibana"
end tell'

sleep 30s


echo "run Vega Server"
osascript -e 'tell app "Terminal"
    do script "npm install http-server -g;http-server '$path'/vegaFiles --cors"
end tell'

# run kibana then insert stuff
cd ..
#curl -X POST "localhost:5601/api/saved_objects/_import" -H "kbn-xsrf: true" --form file=@$path/toImport/IndexPatterns.ndjson
#curl -X POST "localhost:5601/api/saved_objects/_import" -H "kbn-xsrf: true" --form file=@$path/toImport/Visualisation.ndjson
curl -X POST "localhost:5601/api/saved_objects/_import" -H "kbn-xsrf: true" --form file=@$path/toImport/IndexPatterns_Visualisations.ndjson



#Open kibana
open http://localhost:5601


