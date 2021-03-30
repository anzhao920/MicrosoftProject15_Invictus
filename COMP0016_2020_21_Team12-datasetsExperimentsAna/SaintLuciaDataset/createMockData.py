import pandas as pd
import random

MIN_YEAR = 1887
MAX_YEAR = 2018


def getRandomSpeed():
    return random.randrange(4)

def getWindSpeed(year, month):
    year = int(year)
    month = int(month)
    if year >= MIN_YEAR and year <= MAX_YEAR:
        val = monthlyWindSpeedDf._get_value(year - MIN_YEAR, month + 1, takeable=True)
        return val

def getRandomDirection():
    return random.randrange(360)

def loadMeanMonthlyWindSpeedData(filepath):
    return pd.read_csv(filepath)

if __name__ == "__main__":
    speeds = []
    directions = []
    windSpeeds = []

    saintLuciaCSVFileName = 'SaintLuciaWOD_CSV_NOAPI'
    datasetsFilePath = 'D:\AKwork2020-2021\COMP0016\project15\COMP0016_2020_21_Team12\datasets\csvDatasets\\'
    saintLuciaCSVFilePath = 'D:\AKwork2020-2021\COMP0016\project15\COMP0016_2020_21_Team12\SaintLuciaDataset\SaintLuciaWOD_CSV_NOAPI.csv'
    saintLuciaDf = pd.read_csv(saintLuciaCSVFilePath)
    weatherCSVFilePath = "D:\AKwork2020-2021\COMP0016\project15\COMP0016_2020_21_Team12\datasets\csvDatasets\HEW_MOCK_MEAN_MONTHLY_WINDSPEED_1887_2018.csv"
    monthlyWindSpeedDf = loadMeanMonthlyWindSpeedData(weatherCSVFilePath)

    for ind in saintLuciaDf.index:
        speeds.append(getRandomSpeed())
        windSpeeds.append(getWindSpeed(saintLuciaDf['Year'][ind], saintLuciaDf['Month'][ind]))
        directions.append(getRandomDirection())

    saintLuciaDf.rename(columns={'WOD_unique': 'FADIds'}, inplace=True)

    saintLuciaDf['speed'] = speeds
    saintLuciaDf['direction'] = directions
    saintLuciaDf['windSpeed'] = windSpeeds

    mockedFilePath = datasetsFilePath + saintLuciaCSVFileName + 'Mocked' + '.csv'
    saintLuciaDf.to_csv(mockedFilePath)
