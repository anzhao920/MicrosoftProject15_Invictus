import pandas as pd
import json
dataLatLngYear = {}

def addValueFromLatLngYear(lat, lng, year, column, value):
    if ('Unnamed' in column):
        # Rename the unnamed column to index.
        column = 'Index'
    if not (lat in dataLatLngYear):
        dataLatLngYear[lat] = {}
    if not (lng in dataLatLngYear[lat]):
        dataLatLngYear[lat][lng] = {}
    if not (year in dataLatLngYear[lat][lng]):
        dataLatLngYear[lat][lng][year] = {}
        dataLatLngYear[lat][lng][year]['Latiutude'] = str(lat)
        dataLatLngYear[lat][lng][year]['Longitude'] = str(lng)
        dataLatLngYear[lat][lng][year]['Year'] = str(year)

    dataLatLngYear[lat][lng][year][column] = str(value)

def updateDataGivenCSVDataset(datasetPath, datasetName):
    df = pd.read_csv(datasetPath)
    columnNames = df.columns
    for ind in df.index:
        lat = df['Latitude'][ind]
        lng = df['Longitude'][ind]

        if datasetName == 'table1_2015':
            year = 2015
        elif datasetName == 'table1_2016':
            year = 2016
        else:
            year = df['Year'][ind]
        for column in columnNames:
            if (column != 'Year' and column != 'Latitude' and column != 'Longitude' and
            not('qc_flag' in column) and not('dum' in column)):
                addValueFromLatLngYear(lat, lng, year, column, df[column][ind])

def updateDataGivenMeteoDatase(datasetPath):
    df = pd.read_csv(datasetPath)
    for ind in df.index:
        lat = df['Latitude'][ind]
        lng = df['Longitude'][ind]
        for year in range(2000, 2011):
            addValueFromLatLngYear(lat, lng, year, 'Precipitation', df[str(year) + '_tot'][ind])

csvDatasetPath = 'D:\AKwork2020-2021\COMP0016\project15\COMP0016_2020_21_Team12\datasets\csvDatasets\SaintLuciaMocked_csv.csv'
csvDatasetName = 'SaintLuciaMocked_csv'
meteoCsvDatasetPath = 'D:\AKwork2020-2021\COMP0016\project15\COMP0016_2020_21_Team12\datasets\csvDatasets\Met_stations.csv'
updateDataGivenCSVDataset(csvDatasetPath, csvDatasetName)
#updateDataGivenCSVDataset("D:\AKwork2020-2021\COMP0016\project15\COMP0016_2020_21_Team12\datasets\csvDatasets\table1_2015.csv", 'table1_2015')
updateDataGivenMeteoDatase(meteoCsvDatasetPath)

jsonFileName = 'SaintLuciaData_NOAPI_json.json'
jsonFile = open(jsonFileName, 'w')
jsonList = []
for lat in dataLatLngYear:
    for lng in dataLatLngYear[lat]:
        for year in dataLatLngYear[lat][lng]:
            jsonList.append(dataLatLngYear[lat][lng][year])

json_string = json.dumps(jsonList, indent = 4)
json_string_Ex = json.dumps(jsonList[len(jsonList) - 1], indent = 4)
jsonEx = open('SaintLuciaDataEx_json.json', 'w')
json.dump(json_string_Ex, jsonEx)
json.dump(json_string, jsonFile)
jsonEx.close()
jsonFile.close()



