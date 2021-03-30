import pandas as pd
import os
from pathlib import Path, PurePosixPath
import json

def setFADData():
    global FAD_df
    global columns
    FAD_df = getFADDf()
    FAD_df = FAD_df.rename(columns={"Cruise_ID": "FADId"})
    columns = FAD_df.columns

def getFADDf():
    filePath = "data" + os.path.sep + "SaintLuciaWOD_CSV_NOAPI.csv"
    # filePath = 'D:\AKwork2020-2021\COMP0016\project15\COMP0016_2020_21_Team12\SaintLuciaDataset\SaintLuciaWOD_CSV_NOAPI.csv'
    print(filePath)
    return pd.read_csv(filePath)

def addMissingColumns(res):
    newRes = {}
    for col in columns:
        if not(col in res):
            newRes[col] = None
        else:
            newRes[col] = res[col]
    return newRes

def addFAD(fadData):
    global FAD_df
    fadData = addMissingColumns(fadData)
    newRow = pd.DataFrame.from_dict([fadData])
    FAD_df = pd.concat([FAD_df, newRow], ignore_index=True)
    return FAD_df


def convertDFRowToListOfDict(df):
    result = []
    resCount = len(df.index)
    columnNames = df.columns
    for idx in range(0, resCount):
        result.append({})
        for colName in columnNames:
            if isinstance(df.iloc[idx][colName], str):
                result[idx][colName] = df.iloc[idx][colName]
            elif not("nan" in str(df.iloc[idx][colName]).lower()) and not("none" in str(df.iloc[idx][colName]).lower()):
                result[idx][colName] = float(str(df.iloc[idx][colName]))
            else:
                result[idx][colName] = 0

    return result

def getAllFADs():
    global FAD_df
    FAD_df = FAD_df.rename(columns={"Cruise_ID": "FADId"})
    return convertDFRowToListOfDict(FAD_df.head(100))

def findFadById(fadId):
    fad = FAD_df.loc[FAD_df['FADId'] == fadId]
    if fad.empty:
        return None
    return convertDFRowToListOfDict(fad)
