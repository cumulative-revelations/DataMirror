import csv
import json
import ast
import codecs
from zipfile import ZipFile
import os

dirpath = os.getcwd()

def fct():

  # Duplicated or no files?
  count = len([name for name in os.listdir(dirpath+'/script/dataSource') if name.endswith(".zip") and "_LinkedInDataExport_" in name])
  if count == 0:
     print ("No LinkedIn Data")
  elif count > 1:
     print ("Duplicated LinkedIn File")
  else:
    # Get the file, unzip and fix it
    for r, d, f in os.walk(dirpath+"/script/dataSource"):
      for file in f:
        #if file.endswith(".zip") and file.startswith("Basic_LinkedInDataExport_"):
        if file.endswith(".zip") and "_LinkedInDataExport_" in file:
          inputFolderZipped = os.path.join(r,file)

          inputFolder = dirpath+'/script/dataSource/LinkedIn_data'
          if not os.path.exists(inputFolder):
             os.mkdir(inputFolder)

          #with zipfile.ZipFile(inputFolderZipped, 'r') as zip_ref:
          #   zip_ref.extractall(inputFolder)

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
          jsonInputFolder = dirpath+'/script/dataSource/json-LinkedIn_data'
          if not os.path.exists(jsonInputFolder):
             os.mkdir(jsonInputFolder)


          for r, d, f in os.walk(inputFolder):
            file_path = r.replace(inputFolder,jsonInputFolder)
            if not os.path.exists(file_path):
              os.mkdir(file_path)
              
          # root, d=directories, f = files
          for r, d, f in os.walk(inputFolder):
            file_path = r.replace(inputFolder,jsonInputFolder)
            for file in f:
              if file in ["Profile.csv","Connections.csv","Education.csv","Positions.csv","Skills.csv"]: #file.endswith(".csv")
                with codecs.open(os.path.join(r, file), 'r', encoding='utf8') as f_csv: #encoding='utf8'  mac_roman ISO-8859-1
                  reader = csv.DictReader(f_csv)
                  rows = list(reader)

                  json_data = json.dumps(list(rows))
                  json_arr = ast.literal_eval(json_data)

                  json_str=""
                  for i in range(len(json_arr)):
                     json_str = json_str + str(json.dumps(json_arr[i])) + "\n"

                  newFile = file.split('.')[0]+'.json'

                  with codecs.open(os.path.join(file_path,newFile), 'w', encoding='utf8') as f_json:
                     f_json.write(json_str)
                  f_json.close()


