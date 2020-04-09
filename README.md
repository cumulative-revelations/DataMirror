# DataMirror
DataMirror is a tool that enables social network users to aggregate their online data so that they can search, browse and visualise what they have put online.

Currently, DataMirror can be downloaded from Github and Run localy on macOS machine.
The software version on Docker is on progress, and to be shared soon, what can make the software runnable on any OS. 

Steps to use DataMirror:
- Download your data from: <br/>
  Facebook (https://www.facebook.com/help/1701730696756992?helpref=hc_global_nav) <br/>
  Twitter (https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive) <br/>
  LinkedIn (https://www.linkedin.com/pulse/how-download-your-linkedin-archive-judy-schramm/) <br/>
- Do not Change anything in the downloaded data files, do not change the name, do not Unzip, and do not Unzip then zip the file, you keep them as they are, It's very important.
- Put your downloaded data files in the folder: script/dataSource
- Then, in your terminal, run the shell file: sudo sh runThat.sh, that command will install the requirements, elasticsearch and kibana, run them, then it process the data, and create the visualisations.
- At the end, a browser will automatically open, it will show the Indexes, the Index Patterns and the Visualisations, and a Dashboard.

Notes:
- Three terminals will open automatically, at some point, to run elasticsearch, kibana and a local server, they must remain open while working, unless you need to re-run the runThat.sh file, then, they must be closed.
- We added some waiting time in the runThat.sh file, to give time to some copmmands to be "done", therefore, you might find it a bit slow, just be patient.
- Finally, If you had any errors, please contact us.
- You might need to add to the file "kibana.yml" the line: vega.enableExternalUrls: true



