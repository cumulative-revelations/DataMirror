#Created on Wed Dec 25 12:47:44 2019
#@author: Amal Htait


#!/bin/sh

path=${PWD}

# run elasticsearch ( delete its content when testing )
echo "run elasticsearch"
osascript -e 'tell app "Terminal"
    do script "cd '$path'/elasticsearch; bin/elasticsearch"
end tell'

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
curl -X POST "localhost:5601/api/saved_objects/_import" -H "kbn-xsrf: true" --form file=@$path/toImport/IndexPatterns_Visualisations.ndjson



#Open kibana
#open http://localhost:5601
open http://localhost:5601/app/kibana\#/dashboards\?\_g\=\(\)

