# DataMirror
DataMirror: A tool that enables social network users to aggregate their online data so that they can search, browse and visualise what they have put online.


Steps:
1- Download your data from Facebook and Twitter.
2- Do not Change anything in the downloaded data files, do not change the name, do not Unzip, and do not Unzip then zip the file, you keep them as they are, It's very important.
3- Put your downloaded data files in the folder: script/dataSource
4- Then, in your terminal, run the shell file: runThat.sh (you might need a sudo: sudo sh runThat.sh)
5- At the end, a browser will automatically open, it will show the Indexes, the Index Patterns and the Visualisations, you can look up and see the visualisation in "Visualize".

Notes:
- Two terminals will open automatically, at some point, to run elasticsearch and kibana, they must remain open while working, unless you need to re-run the runThat.sh file, then, they must be closed.
- I added some waiting time in the runThat.sh file, to give time to some copmmands to be "done", therefore, you might find it a bit slow, just be patient.
- Finally, If you had any errors, please send me screenshots.
