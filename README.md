# SteelEye-DataEnginneer-Assessment
# Assigment for SteelEye Data Engineer Assessment

Link for the csv file : https://steeleye-bucket-1.s3.ap-south-1.amazonaws.com/final-data.csv

Submitted by - Vedansh Nigam

# Components:
- setup.py : installs necessary python modules
- bucket.py : This file was only execute once. The purpose was to create a S3 bucket on my AWS account
- main.py : Python file containing the code
- main.log : Log file to monitor functioning and for debugging
- data.xml : This will be created on execution. Needs to be parsed to fetch the download link
- DLTINS_20210117.zip : Zipped file downloaded from the extracted link. Ideally it should be downloaded using python
                        but i have downloaded it manually.
- DLTINS_20210117.xml : File extracted from the zip
- dataset.csv : Data extracted from the xml file as per the requirement.           
          
# Instructions: 
- Dowload the folder as zip
- Please make sure that the DLTINS_20210117.zip file is present before starting execution
- Run the setup.py file to ensure all Requirements are met
- Run the main.py file

# Requirements achieved : 
- Parsing the xml file
- Extracting the download link
- Parsing the second xml file 
- Extracting data
- Storing the extracted data as a csv file
- Uploading the csv to an Amazom S3 bucket

# Limitations :
- Had to manually download the zip file from the extracted download link
- AWS bucket had to be created manually
- Unit Tests are not present
