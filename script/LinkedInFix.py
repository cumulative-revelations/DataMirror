import csv
import json
import ast
import codecs
from zipfile import ZipFile
import os


def fct():
  # Duplicated or no files?
  count = len([name for name in os.listdir('dataSource') if name.endswith(".zip") and name.startswith("Basic_LinkedInDataExport_")])
  if count == 0:
     print ("No LinkedIn Data")
  elif count > 1:
     print ("Duplicated LinkedIn File")

  # Get the file, unzip and fix it
  for r, d, f in os.walk("dataSource"):
    for file in f:
      if file.endswith(".zip") and file.startswith("Basic_LinkedInDataExport_"):

        inputFolderZipped = os.path.join(r,file)

        inputFolder = 'dataSource/LinkedIn_data'
        if not os.path.exists(inputFolder):
        	os.mkdir(inputFolder)

        #with zipfile.ZipFile(inputFolderZipped, 'r') as zip_ref:
        #	zip_ref.extractall(inputFolder)

        print ("LinkedIn - Unzip ")

        # Create a ZipFile Object and load sample.zip in it
        with ZipFile(inputFolderZipped, 'r') as zipObj:
           # Get a list of all archived file names from the zip
           listOfFileNames = zipObj.namelist()
           # Iterate over the file names
           for fileName in listOfFileNames:
               # Check filename endswith csv
               if fileName.endswith('.csv'):
                   # Extract a single file from zip
                   zipObj.extract(fileName, inputFolder)




        print ("LinkedIn - Fix")
        jsonInputFolder = 'dataSource/json-LinkedIn_data'
        if not os.path.exists(jsonInputFolder):
        	os.mkdir(jsonInputFolder)


        # root, d=directories, f = files
        for r, d, f in os.walk(inputFolder):
        	#for c in f:
        	for file in f:
            if file.endswith(".csv"): #I can add a list of files
              #subPath = os.path.join(r, file)
                #print ("folder",r)
                with codecs.open(os.path.join(r, file), 'r', encoding='utf8') as f_csv:

                	reader = csv.DictReader(f_csv)
                	rows = list(reader)

                	json_data = json.dumps(list(rows))
                	json_arr = ast.literal_eval(json_data)

                	json_str=""
                	for i in range(len(json_arr)):
                		json_str = json_str + str(json.dumps(json_arr[i])) + "\n"

                	newFile = file.split('.')[0]+'.json'
                	r_parts = r.split("/")
                	with codecs.open(os.path.join(r_parts[0]+"/json-"+r_parts[1],newFile), 'w', encoding='utf8') as f_json:
                		f_json.write(json_str)
                	f_json.close()

