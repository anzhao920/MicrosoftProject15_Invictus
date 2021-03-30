import pandas as pd
import pointInPolygon

def getSaintLuciaPolygonFromFile():
    #File that contains the coordinates of the polygon on separate line, in format 'lat lng'.
    coordsFilePath = "StLuciaCoords.txt"
    coordsFile = open(coordsFilePath, "r")
    points = []
    while True:
        line = coordsFile.readline()
        if not(line):
            break
        line = line.split(",")
        points.append((float(line[0]), float(line[1])))
    return pointInPolygon.Polygon(points)


def isPointInSaintLuciaPoly(SaintLuciaPoly, lat, lng):
    p = (float(lat), float(lng))
    return SaintLuciaPoly.contains(p)

def filterCSVForSaintLucia():
    SaintLuciaPoly = getSaintLuciaPolygonFromFile()
    locationsDataCSVFilePath = "D:\AKwork2020-2021\COMP0016\project15\COMP0016_2020_21_Team12\datasets\csvDatasets\OSDO7106CSV.csv"
    wodDf = pd.read_csv(locationsDataCSVFilePath)
    SaintLuciaDf = pd.DataFrame(columns=wodDf.columns)
    # Dictionary that stores geographical information for each point in the WOD csv.
    nRows = 0
    dataLatLng = {}
    for ind in wodDf.index:
        lat = wodDf['Latitude'][ind]
        lng = wodDf['Longitude'][ind]
        if not (lat in dataLatLng):
            dataLatLng[lat] = {}
        if not (lng in dataLatLng[lat]):
            dataLatLng[lat][lng] = isPointInSaintLuciaPoly(SaintLuciaPoly, lat, lng)
        if dataLatLng[lat][lng]:
            # Add points corresponding to Saint Lucia to SaintLuciaDf.
            SaintLuciaDf.loc[nRows] = wodDf.loc[ind]
            nRows += 1

    #The r flag is necessary s.t. backslashes are not considered special characters.
    filterdCSVFilePath = r'SaintLuciaWOD_CSV_NOAPI_new.csv'
    SaintLuciaDf.to_csv(filterdCSVFilePath)
    print(SaintLuciaDf.columns)
    print(nRows)

if __name__ == "__main__":
    filterCSVForSaintLucia()

