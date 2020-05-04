# DataMirror
DataMirror is a tool that enables social network users to aggregate their online data so that they can search, browse and visualise what they have put online.

Currently, DataMirror can be downloaded from Github and Run localy on macOS and Linux (Ubuntu) machines.
The software version on Docker is on progress, and to be shared soon, what can make the software runnable on any OS. 

Steps to use DataMirror:
- Request your Online Data from the following Online Social Media (Note that this might take some time): <br/>
  Facebook (https://www.facebook.com/help/1701730696756992?helpref=hc_global_nav) <br/>
  Twitter (https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive) <br/>
  LinkedIn (https://www.linkedin.com/pulse/how-download-your-linkedin-archive-judy-schramm/) <br/>
  PS: Do not Change anything in the downloaded data files, do not change the name, do not Unzip, and do not Unzip then zip the   file, you keep them as they are, It's very important.
- Download or Clone the current Github repository called "DataMirror".
- Put your downloaded Social Media data files in the folder: Local_Path_to_DataMirror/DataMirror/script/dataSource
- Then, in a terminal, run the following shell file to setup DataMirror:  <br/> 
    sudo sh X_preRun_DataMirror.sh  <br/>
  With X as Linux or macOS.
  This commands would install the requirements, elasticsearch and kibana.
  PS: You might need to add to the file "kibana.yml" the line: vega.enableExternalUrls: true
      (In Ubuntu: /etc/kibana/kibana.yml)
- Then, to run the tool, run the follwing shell file:
    sudo sh X_Run_DataMirror.sh  <br/>
    With X as Linux or macOS.
    This command would run elasticsearch and kibana, then it process the data, and create the visualisations.
- At the end, a browser will automatically open (http://localhost:5601/), it will show the Dashboard of Visualisation.

Notes:
- Some terminals will open automatically, at some point, to run elasticsearch, kibana or a local server, they must remain open while working, unless you need to re-run the runThat.sh file, then, they must be closed.
- We added some waiting time in the sh file, to give time to some copmmands to be "done", therefore, you might find it a bit slow, just be patient.
- Finally, If you had any errors, please comment or contact us : amal.htait@strath.ac.uk




