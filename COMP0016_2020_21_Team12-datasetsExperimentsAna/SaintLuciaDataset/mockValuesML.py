from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
import math
import statistics

EPS = 0.00000001
#Change the type to "linearRegression" for using the linear regression model.
modelType = 'SVM'

""" Raises ValueError exception if the string is not a number or the number otherwise. """
def number(x):
    try:
        x = float(x)
        if not(math.isnan(float(x))):
            return x
        raise ValueError("NaN values should not be considered")
    except ValueError:
        raise ValueError("No value provided")

def loadMeanMonthlyWindSpeedData(filepath):
    return pd.read_csv(filepath)

def getMinMaxForX(x):
    minX = [x[0][0], x[0][1]]
    maxX = [x[0][0], x[0][1]]
    for i in range(1, len(x)):
        for j in range(len(x[i])):
            minX[j] = min(minX[j], x[i][j])
            maxX[j] = max(maxX[j], x[i][j])

    return minX, maxX
def getMeanAndSTD(x):
    x1 = []
    x2 = []
    for i in range(len(x)):
        x1.append(x[i][0])
        x2.append(x[i][1])
    return [statistics.mean(x1), statistics.mean(x2)], [statistics.pstdev(x1), statistics.pstdev(x2)]


def normalizeMinMax(minX, maxX, x):
    for i in range(len(x)):
       for j in range(len(x[i])):
           x[i][j] = (x[i][j] - minX[j]) / (maxX[j] - minX[j] + EPS)
    return x

def normalize(mean, stdev, x):
    for i in range(len(x)):
       for j in range(len(x[i])):
           x[i][j] = (x[i][j] - mean[j]) / stdev[j]
    return x

def splitData(X, Y, trainP):
    n = len(Y)
    sz1 = int(float(n * trainP / 100))
    xTrain = []
    xTest = []
    yTrain = []
    yTest = []
    for i in range(n):
        if i < sz1:
            xTrain.append(X[i])
            yTrain.append(Y[i])
        else:
            xTest.append(X[i])
            yTest.append(Y[i])
    return xTrain, xTest, yTrain, yTest

def testModel(modelName, regressionModel, xTest, yTest):
    yPred = regressionModel.predict(xTest)
    result1 = mean_absolute_error(yTest, yPred)
    result2 = r2_score(yTest, yPred)
    print("Testing model " + modelName + ": mean absolute error is " + str(result1) + " and R2 score is " + str(result2))

def createLinearRegressionModel(X, Y):
    linearRegressionModel = LinearRegression()
    mean, stdev = getMeanAndSTD(x)
    normX = normalize(mean, stdev, X)
    xTrain, xTest, yTrain, yTest = splitData(normX, Y, 70)
    linearRegressionModel.fit(xTrain, yTrain)
    testModel("linear regression", linearRegressionModel, xTest, yTest)
    return mean, stdev, linearRegressionModel


def createSVMModel(X, Y):
    mean, stdev = getMeanAndSTD(x)
    svmRegressionModel = svm.SVR(kernel='rbf')
    normX = normalize(mean, stdev, X)
    xTrain, xTest, yTrain, yTest = splitData(normX, Y, 70)
    svmRegressionModel.fit(xTrain, yTrain)
    testModel("SVM", svmRegressionModel, xTest, yTest)
    return mean, stdev, svmRegressionModel

def addMockWindSpeedForPastYears(x, y, MIN_YEAR, MAX_YEAR):
    global monthlyWindSpeedDf
    if modelType == 'SVM':
        mean, stdev, regressionModel = createSVMModel(x, y)
    elif modelType == 'linearRegression':
        mean, stdev, regressionModel = createLinearRegressionModel(x, y)
    else:
        print('Invalid model type')
        exit(-1)

    columnNames = monthlyWindSpeedDf.columns

    for year in range(MAX_YEAR - 1, MIN_YEAR - 1, -1):
        coulmnValues = [year]
        for month in range(12):
            coulmnValues.append(round(regressionModel.predict(normalize(mean, stdev, [[year, month]]))[0]))
        assert (len(coulmnValues) == 13)
        # Add the predicted values for current year to the top of monthlyWindSpeedDf data frame.
        rowDf = pd.DataFrame([coulmnValues], columns = columnNames)
        monthlyWindSpeedDf = pd.concat([rowDf, monthlyWindSpeedDf], ignore_index=True)

if __name__ == "__main__":
    csvDataFilePath = r"D:\AKwork2020-2021\COMP0016\project15\COMP0016_2020_21_Team12\datasets\csvDatasets\HEW_MEAN_MONTHLY_WINDSPEED_1973-Apr_2018.csv"
    monthlyWindSpeedDf = loadMeanMonthlyWindSpeedData(csvDataFilePath)

    # x is a list of list in format [[year0, month0], [year1, month1], ... ]
    x = []
    # y is a list containing the wind speed, i.e. y[i] = wind speed for year x[i][0] and mont x[i][1]
    y = []

    for index in monthlyWindSpeedDf.index:
        year = monthlyWindSpeedDf['Unnamed: 0'][index]
        for month in range(12):
            try:
                windSpeed = number(monthlyWindSpeedDf._get_value(index, month + 1, takeable=True))
                x.append([year, month])
                y.append(windSpeed)
            except ValueError:
                continue

    addMockWindSpeedForPastYears(x, y, 1887, 1973)
    enhancedDataFilePath = r"D:\AKwork2020-2021\COMP0016\project15\COMP0016_2020_21_Team12\datasets\csvDatasets\HEW_MOCK_MEAN_MONTHLY_WINDSPEED_1887_2018.csv"
    monthlyWindSpeedDf.to_csv(enhancedDataFilePath)
