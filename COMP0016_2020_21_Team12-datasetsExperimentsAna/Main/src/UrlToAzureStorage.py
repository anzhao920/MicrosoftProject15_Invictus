import os
import requests
import mmap
import gzip
import csv
import json
import sys
import subprocess
import platform
import re

from azure.storage.blob import BlobServiceClient, BlobClient, BlobClient, ContainerClient
from dotenv import load_dotenv
from urllib.parse import urlparse
from datetime import datetime

# Auxilary functions
def executeCProgram(CprogramFileName, systemType):
    command = []
    if 'Linux' in systemType:
        subprocess.call(["gcc", CprogramFileName, '-o', 'Cprogram'])  # For Compiling
        command = ['./Cprogram']
    elif 'Windows' in systemType:
        subprocess.call(["gcc", CprogramFileName])
        subprocess.call('a.exe')
        command = ['./Cprogram']
    elif 'Darwin' in systemType:
        subprocess.call(["gcc", CprogramFileName])
        command = ['./a.out']
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.communicate(input='dataToReadFile.txt\n'.encode())[0]


def writeInputForParser(WODFileName, CSVFileName):
    dataToReadFile = open("dataToReadFile.txt", "w")
    dataToReadFile.write(WODFileName + "\n")
    dataToReadFile.write("0\nA\n")
    dataToReadFile.write(CSVFileName + "\n1\n")
    dataToReadFile.close()

def ungz(filename):
    fname = filename.replace(".gz", "")
    gfile = gzip.GzipFile(filename)
    open(fname, "wb+").write(gfile.read())
    gfile.close()
    
def tidyname(filename):
    pattern = '[A-Za-z][A-Za-z0-9]'
    tidy_name = "".join(re.findall(pattern, os.path.splitext(filename)[0]))
    
    if len(tidy_name) > 63:
        tidy_name = tidy_name[:63]
    elif len(tidy_name) < 3:
        tidy_name = tidy_name + datetime.now().strftime("%H%M%S")
     
    return tidy_name

def get_credentials():
    load_dotenv()
    return os.getenv('AZURE_CONNECTION_STRING'), os.getenv("AZURE_CONTAINER_NAME")

# Main function
def uploadToBlob():
    connection_string, container_name = get_credentials()
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    containerclient = blob_service_client.get_container_client(container_name)
    # Give the filecontent here
    filecontent = ["https://data.govt.lc/sites/default/files/Estimated%20fish%20landings.csv"]
    print(f'Copying ' + str(len(filecontent)) + ' Blobs from URL')

    for content in filecontent:
        url = urlparse(content)
        u = requests.get(content, stream=True)
        filename = os.path.basename(url.path)
        pre, ext = os.path.splitext(filename)
        updated_filename = tidyname(pre) + ".json"
        
        # This checks if a blob is already existed
        blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=updated_filename)
        if blob.exists():
            blob.delete_blob(delete_snapshots=False)
        
        # If a gz file is downloaded, unzip it and decode it into a csv file
        if ext == ".gz":
            with open(filename, 'wb') as f:
                f.write(u.content)
            ungz(filename)
            CprogramFileName = "wodtodepthmatrix.c"
            WODFileName = pre
            filename = WODFileName + ".csv"
            # Creates the csv file named as filename
            writeInputForParser(WODFileName, filename)
            executeCProgram(CprogramFileName, platform.system())
            # Remove the unzipped file and downloaded gz file
            os.remove(os.path.abspath(WODFileName + ".gz"))

        # If a csv file is downloaded, creates a csv file
        if ext == ".csv":
            with open(filename, "wb") as f:
                f.write(u.content)

        # Converts the csv file into a Json file
        with open(filename, "r+b") as f:
            mm = mmap.mmap(f.fileno(), 0)   
            mm.seek(0)
            ls = []
            for i in range(mm.size()):
                byte = mm.readline()
                line = byte.decode('utf-8', 'ignore')
                line = line.strip()
                line = line.split(',')
                line = list(filter(lambda a: a != '', line))
                if len(line) == 0:
                    continue
                ls.append(line)
            
            for i in range(1, len(ls)):
                ls[i] = dict(zip(ls[0], ls[i]))
            in_json = json.dumps(ls[1:], indent=4)
            
            # Connects to the cilent and upload the data to the Blob
            blob_client = containerclient.get_blob_client(updated_filename)
            blob_client.upload_blob(in_json, metadata=None)
            # Removes the csv file created
            os.remove(os.path.abspath(filename))
            if os.path.exists(pre):
                os.remove(os.path.abspath(pre))
            f.close()
            mm.close()          
            
    print("Operation started. Closing application.")

if __name__ == '__main__':
    uploadToBlob()