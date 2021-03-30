import countries
import pandas as pd
cc = countries.CountryChecker('TM_WORLD_BORDERS-0.3.shp')

wodDf = pd.read_csv("datasets\csvDatasets\OSDO7106CSV.csv")
SaintLuciaDf = pd.DataFrame(columns=wodDf.columns)

def getCountryISOFromLatLng(lat, lng):
  if cc.getCountry(countries.Point(lat, lng)):
    return cc.getCountry(countries.Point(lat, lng)).iso
  return ''

nRows = 0
for ind in wodDf.index:
  lat = wodDf['Latitude'][ind]
  lng = wodDf['Longitude'][ind]
  if (getCountryISOFromLatLng(lat, lng) == 'LC'):
    SaintLuciaDf.loc[nRows] = wodDf.loc[ind]
    nRows += 1

SaintLuciaDf.to_csv(r'SaintLuciaWOD_CSV.csv')
print(nRows)
