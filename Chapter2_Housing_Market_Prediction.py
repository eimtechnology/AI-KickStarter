import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Stpe1
# Load the dataset
data = pd.read_csv('vancouver_housing_price.csv')

# Display the first few rows of the dataset
# print(data.head())

# Step2
fig = plt.figure(figsize=(10, 10))

# Scatter plot for Price vs Income
fig1 = plt.subplot(231)
plt.scatter(data['Avg. Area Income'], data['Price'])
plt.title('Price VS Income')

# Scatter plot for Price vs House Age
fig2 = plt.subplot(232)
plt.scatter(data['Avg. Area House Age'], data['Price'])
plt.title('Price VS House Age')

# Scatter plot for Price vs Number of Rooms
fig3 = plt.subplot(233)
plt.scatter(data['Avg. Area Number of Rooms'], data['Price'])
plt.title('Price VS Number of Rooms')

# Scatter plot for Price vs Area Population
fig4 = plt.subplot(234)
plt.scatter(data['Area Population'], data['Price'])
plt.title('Price VS Area Population')

# Scatter plot for Price vs Size
fig5 = plt.subplot(235)
plt.scatter(data['size'], data['Price'])
plt.title('Price VS Size')
#display
plt.show()

# Step3
# Define X and y
X = data['size']
y = data['Price']
#print(y.head())


# Reshape X for model training
X = np.array(X).reshape(-1, 1)
# print(X.shape)

# Set up the linear regression model
LR1 = LinearRegression()

# Train the model
LR1.fit(X, y)

# Calculate predicted prices
y_predict_1 = LR1.predict(X)

#print the first 5 rows of X and y_predict_1 to see the predicted prices
print(X[0:5])
print(y[0:5])
print(y_predict_1[0:5])

# Step4
# generate a plot of the actual prices and the predicted prices
fig6 = plt.figure(figsize=(8,5))
plt.scatter(X,y)
plt.plot(X,y_predict_1,'r')
plt.show()

# Evaluate the model by calculate MSE and R2
mean_squared_error_1 = mean_squared_error(y, y_predict_1)
r2_score_1 = r2_score(y, y_predict_1)
print("The mean squared error is",mean_squared_error_1,"and the r2 score is",r2_score_1)

# Step5
#define X_multi
X_multi = data.drop(['Price'],axis=1)
X_multi

#set up 2nd linear model
LR_multi = LinearRegression()
#train the model
LR_multi.fit(X_multi,y)

#make prediction
y_predict_multi = LR_multi.predict(X_multi)
print(y_predict_multi)


#generate a new plot of the actual prices and the predicted prices
fig7 = plt.figure(figsize=(8,5))
plt.scatter(y,y_predict_multi)
plt.show()

fig7 = plt.figure(figsize=(8,5))
plt.scatter(y,y_predict_1)
plt.show()

#evaluate the model
mean_squared_error_multi = mean_squared_error(y,y_predict_multi)
r2_score_multi = r2_score(y,y_predict_multi)
print("The mean squared error is",mean_squared_error_multi,"and the r2 score is",r2_score_multi)

#make a prediction for a new data point
X_test = [55000,5,5,30000,200]
X_test = np.array(X_test).reshape(1,-1)
print(X_test)

#make a prediction for a new data point
y_test_predict = LR_multi.predict(X_test)
print(y_test_predict)
