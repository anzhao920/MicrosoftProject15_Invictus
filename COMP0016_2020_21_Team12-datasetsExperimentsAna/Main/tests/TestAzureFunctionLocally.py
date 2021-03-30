import logging
import json
import os
import re

from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, BlobClient, ContainerClient, ContentSettings
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tableservice import TableService, AzureHttpError
from azure.cosmosdb.table.tablebatch import TableBatch
from dotenv import load_dotenv


filename = "Estimatefishlandings.json"
tablename = "Estimatefishlandings" + datetime.now().strftime("%H%M%S")
fixed_tablename = tablename
partition_key = 'Fishlanding'

def list_of_groups(init_list, childern_list_len):
    list_of_group = zip(*(iter(init_list),) *childern_list_len)
    end_list = [list(i) for i in list_of_group]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    
    return end_list

def get_credentials():
    load_dotenv()
    return os.getenv('AZURE_CONNECTION_STRING'), os.getenv("AZURE_CONTAINER_NAME")

def uploadToTable():
    connection_string, container_name = get_credentials()
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=filename)
    blob_data = blob.download_blob().readall()
    json_file_content = blob_data.decode('utf8')
    jlist = json.loads(json_file_content)

    table_service = TableService(connection_string=connection_string)
    table_service.create_table(table_name=fixed_tablename)

    partition_key = 'Fishlanding'
    row = 1

    batch_list = []
    for jdict in jlist:
        task = {'PartitionKey': partition_key, 'RowKey': str(row)}
        for key in jdict:
            keyVal = key.replace(' ', '')
            if keyVal == '':
                pass
            task[keyVal] = jdict[key]
        batch_list.append(task)
        row += 1
        
    seperated_batch_list = list_of_groups(init_list=batch_list, childern_list_len=50)
    for children_list in seperated_batch_list:
        batch = TableBatch()
        for task in children_list:
            batch.insert_or_replace_entity(task)
        table_service.commit_batch(table_name=tablename, batch=batch)
    
    return batch_list

def getFromTable(wanted_keys, num_results):
    connection_string, container_name = get_credentials()
    table_service = TableService(connection_string=connection_string)
    
    tasks = list(table_service.query_entities(table_name=fixed_tablename, filter="PartitionKey eq 'Fishlanding'", num_results=num_results))
    dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
    result_list = []
    
    for task in tasks:
        result_list.append(dictfilt(task, wanted_keys))
    
    return result_list

if __name__ == "__main__":
    upload_list = uploadToTable()
    wanted_keys = set(upload_list[0].keys())
    num_results = len(upload_list)
    downloaded_list = getFromTable(wanted_keys=wanted_keys, num_results=num_results)
    sorted_upload_list = json.loads(json.dumps(upload_list, sort_keys=True))[:100]
    sorted_downloaded_list = json.loads(json.dumps(downloaded_list, sort_keys=True))
    
    print(sorted_downloaded_list == sorted_downloaded_list)