# We are gonna use Scikit's LinearRegression model
from sklearn.linear_model import LinearRegression

# Your input data, X and Y are lists (or Numpy Arrays)
x = [[2,4],[3,6],[4,5],[6,7],[3,3],[2,5],[5,2]]
y = [14,21,22,32,15,16,19]

# Initialize the model then train it on the data
genius_regression_model = LinearRegression()
genius_regression_model.fit(x,y)

# Predict the corresponding value of Y for X = [8,4]

assert abs(genius_regression_model.predict([[8,4]])[0] - 32) < 0.1