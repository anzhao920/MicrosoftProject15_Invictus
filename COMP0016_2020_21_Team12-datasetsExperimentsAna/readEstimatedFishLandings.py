import pandas as pd

#estimFishLandings2000_2014 = pd.read_csv("datasets\csvDatasets\EstimatedFishLandings2000-2014.csv")
estimFishLandings2015 = pd.read_csv("datasets\csvDatasets\EstimatedFishLandings2015.csv")
#estimFishLandings2016 = pd.read_csv("datasets\csvDatasets\EstimatedFishLandings2016.csv")
cnt = 0

#Create csv with Table 1: Estimated fish landings for Jan - Dec 2015
def createTable_2015(tableName, columnNamesInex, lastColumnIndex):
    columnNames = []
    data = []
    cnt = 0
    for index, row in estimFishLandings2015.iterrows():
        if index == columnNamesInex:
            for i in range(len(row) - 1):
                columnNames.append(row[i])
        if cnt > columnNamesInex:
            data.append([])
            for column in range(len(columnNames)):
                data[cnt - columnNamesInex - 1].append(row[column])
        cnt += 1
        if cnt > lastColumnIndex:
            break
    table = pd.DataFrame(data, columns = columnNames)
    table.to_csv("datasets/csvDatasets/" + tableName + ".csv", index=False)
    return table

table1 = createTable_2015("table1_2015", 4, 15)
table2 = createTable_2015("table2_2015", 18, 29)
