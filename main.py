# IMPORTING REQUIRED LIBRARIES
import requests
import logging
from zipfile import ZipFile
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
import boto3

# OPENING LOG FILE
def startLog():
    logging.info(datetime.now()) # Storing current time in log
    logging.info('Program started')
    
def endLog():
    logging.info('Program Complete')    

def termLog():
    logging.warning('Program Terminated')   

def errorLog(e):
    logging.error(e)
    termLog()
    
def downloadFile(url,file_name):
  # DOWNLOADING THE REQUIRED XML FILE USING REQUESTS LIBRARY
    file = requests.get(url)
    open(file_name,'wb').write(file.content)   

def findLink(file_name):
    # PARSING THE XML FILE USING ELEMENT TREE MODULE
    import xml.etree.ElementTree as ET
    tree = ET.parse(file_name)
    root = tree.getroot()
    zip_url=" "
    for x in root.iter('str'):
        name=x.attrib['name']
        if name == 'download_link':
            zip_url=x.text
            break
    if zip_url != " ":
        print("ZIP URL: ",zip_url)
        logging.info('Download link found successfully')
        # ZIP FILE HAD TO BE DOWNLOADED MANUALLY
        logging.info('File Downloaded')

    return zip_url     

def unzipFile(file_name):    
            logging.info('Unzipping file')
            with ZipFile(file_name,'r') as zip:
             zip.extractall() 

def createDF(file_name):
    # CREATING COLUMNS AS PER REQUIREMENT
    cols = ["FinInstrmGnlAttrbts.Id", "FinInstrmGnlAttrbts.FullNm", "FinInstrmGnlAttrbts.ClssfctnTp", "FinInstrmGnlAttrbts.CmmdtyDerivInd", "FinInstrmGnlAttrbts.NtnlCcy","Issr"]
    rows = []

    # Parsing the XML file
    tree = ET.parse(file_name)
    root = tree.getroot()
    open=0
    l=[]
    print('Parsing XML .... please wait')
    for x in root.iter(): 


        s=x.tag.split('}') # EXTRACTING SIMPLIFIED TAG NAME FROM THE XML
        if s[-1] == 'Id' and s[0][-1] == '2':
            if open == 0:
                l.append(x.text)
            open = open ^ 1  # CHECKING FOR OPENING AND CLOSING TAGS
        if s[-1] == 'FullNm':
            l.append(x.text)
        if s[-1] == 'ClssfctnTp':
            l.append(x.text)
        if s[-1] == 'CmmdtyDerivInd':
            l.append(x.text)
        if s[-1] == 'NtnlCcy':
            l.append(x.text)
        if s[-1] == 'Issr':
            l.append(x.text)    

        if len(l) == 6:
            l[3],l[4]=l[4],l[3]  # SWAPPING 3RD AND 4TH ELEMENTS DUE TO DIFFERENT ORDERING OF TAGS IN XML
            rows.append(l) # CREATING A LIST OF LISTS
            l=[]  
    print('Parsing complete')          
    logging.info('Data successfully extracted')
    logging.info('Converting data to Data Frame')
    df=pd.DataFrame(rows,columns=cols) # CONVERTING THE EXTRACTED DATA TO A DATAFRAME
    logging.info('Converting data to csv')
    df.to_csv('dataset.csv') # CONVERTING THE DATAFRAME TO A CSV FILE
    logging.info('Converting data to csv successful')
    
def uploadtoAWS(filepath,bucket,filename):
    s3 = boto3.client('s3');
    s3.upload_file(filepath,bucket,filename)

if __name__=='__main__':
    try:
        logging.basicConfig(filename='main.log',filemode='a',format='%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
        startLog()
        url = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100"
        downloadFile(url,'data.xml')
        zip_url = findLink('data.xml')
        unzipFile('DLTINS_20210117_01of01.zip')
        createDF('DLTINS_20210117_01of01.xml')
        # uploadtoAWS('dataset.csv','steeleye-bucket-1','final-data.csv') 
        # The above line has been commented since the csv has already been uploaded to an AWS S3 bucket
    except Exception as e:
        errorLog(e)
    else:
        endLog()    