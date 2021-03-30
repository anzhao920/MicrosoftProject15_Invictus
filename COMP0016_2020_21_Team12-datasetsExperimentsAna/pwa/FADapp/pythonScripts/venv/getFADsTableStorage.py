import os
import json

from azure.cosmosdb.table.tableservice import TableService, AzureHttpError
import pandas as pd

table_name = 'FADDATA'
connection_string = os.getenv('AZURE_CONNECTION_STRING')

def getNumberOfRows():
    return len(getAllFADs())

def addDataToTable(FAD_df, columns, N):
    for i in range(0, N):
        fadEntity = {'PartitionKey': str(FAD_df['Cruise_ID'][i]), 'RowKey': str(i + 1)}
        for col in columns:
            entityCol = col.replace('(', '_').replace(')', '_')
            if 'nan' in str(FAD_df[col][i]) or 'Unnamed' in col:
                continue
            if col == 'Cruise_ID':
                fadEntity['FADId'] = str(FAD_df['Cruise_ID'][i])
                continue
            if not ('qc_flag' in col):
                fadEntity[entityCol] = str(FAD_df[col][i])
        # Add fadEntity to table.
        table_service.insert_entity(table_name, fadEntity)


def loadDataFromCSV():
    filePath = 'D:\AKwork2020-2021\COMP0016\project15\COMP0016_2020_21_Team12\SaintLuciaDataset\SaintLuciaWOD_CSV_NOAPI.csv'
    FAD_df = pd.read_csv(filePath)
    N = min(100, len(FAD_df))
    columns = FAD_df.columns
    addDataToTable(FAD_df, columns, N)

def createFADTable():
    loadDataFromCSV()
    try:
        table_service.create_table(table_name=table_name)
        loadDataFromCSV()
    except:
        print('Table and data already exists!')


def setFADData():
    global table_service
    table_service = TableService(connection_string=connection_string)
    #createFADTable()

def addMissingColumns(res, rowValue):
    for key in res:
        if not (' ' in key):
            continue
        val = res[key]
        res.pop(key)
        key = key.replace(' ', '')
        if key != '':
            res[key] = val
    res['PartitionKey'] = res['FADId']
    res['RowKey'] = rowValue
    # res.pop('FADId', None)
    return res

def addFAD(fadData):
    row = getNumberOfRows()
    fadEntity = addMissingColumns(fadData, row)
    table_service.insert_entity(table_name, fadEntity)

def getAllFADs():
    FADData = table_service.query_entities(table_name)
    FADList = []
    for FAD in FADData:
        FADList.append(FAD)
    return FADList

def removeColumns(entity, columns):
    res = {}
    for key in entity:
        if not (key in columns):
            res[key] = entity[key]
    return res


def findFadById(fadId):
    filterStr = "PartitionKey eq '" + str(fadId) + "'"
    columnsToRemove = ['Timestamp', 'etag']
    FADData = table_service.query_entities(table_name, filter=filterStr)
    FADList = []
    for entity in FADData:
        FADList.append(removeColumns(entity, columnsToRemove))
    if len(FADList) == 0:
        return None
    return FADList
