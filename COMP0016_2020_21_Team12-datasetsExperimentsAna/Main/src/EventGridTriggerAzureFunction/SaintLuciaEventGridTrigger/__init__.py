import json
import os
import re
import time
import azure.functions as func

from datetime import datetime
from azure.storage.blob import BlobClient
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.tablebatch import TableBatch


def main(event: func.EventGridEvent):
    event_type = event.event_type
    event_subject = event.subject
    containername = event_subject.split("/")[-3]
    
    # credentials needed
    connection_string = os.getenv('AZURE_CONNECTION_STRING')
    container_name = os.getenv('ContainerName')
    
    # Only blob creations at container would trigger this function
    if event_type == "Microsoft.Storage.BlobCreated" and containername == container_name:
        filename = event_subject.split("/")[-1]
        tablename = gettablename(filename=filename) + datetime.now().strftime("%H%M%S")
        table_service = TableService(connection_string=connection_string)
        table_service.create_table(table_name=tablename)
        
        # Download the blob data        
        blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=filename)
        blob_data = blob.download_blob().readall()
        json_file_content = blob_data.decode('utf8').replace("'",'"')
        jlist = json.loads(json_file_content)
        
        # The partition key might be changed later. This is only for DEVELOPMENT purpose
        partition_key = tablename
        row = 1
        batch_list = []
        for jdict in jlist:
            if 'Cruise_ID' in jdict:
                partition_key = jdict['Cruise_ID']
            task = {'PartitionKey': partition_key, 'RowKey': str(row)}
            for key in jdict:
                keyVal = key.replace(' ', '')
                if keyVal == '':
                    continue
                task[keyVal] = jdict[key]
            batch_list.append(task)
            row += 1
        
        seperated_batch_list = list_of_groups(init_list=batch_list, childern_list_len=50)
        for children_list in seperated_batch_list:
            batch = TableBatch()
            for task in children_list:
                batch.insert_or_replace_entity(task)
            table_service.commit_batch(table_name=tablename, batch=batch)

def gettablename(filename):
    pattern = '[A-Za-z][A-Za-z0-9]'
    tablename = "".join(re.findall(pattern, os.path.splitext(filename)[0]))
    
    if len(tablename) > 63:
        tablename = tablename[:56]
    return tablename

def list_of_groups(init_list, childern_list_len):
    list_of_group = zip(*(iter(init_list),) *childern_list_len)
    end_list = [list(i) for i in list_of_group]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    
    return end_list