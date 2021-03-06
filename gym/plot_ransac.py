"""
===========================================
Robust linear model estimation using RANSAC
===========================================

In this example we see how to robustly fit a linear model to faulty data using
the RANSAC algorithm.

"""
import numpy as np
import pickle
from matplotlib import pyplot as plt

from sklearn import linear_model, datasets


n_samples = 1000
n_outliers = 1080

with open('data.pickle', 'rb') as f:
    data = pickle.load(f)



# X, y, coef = datasets.make_regression(n_samples=n_samples, n_features=1,
#                                       n_informative=1, noise=10,
#                                       coef=True, random_state=0)

X = [np.arange(0, 1080, 1, dtype=int)]
y = [data]
coef = 0.5

print(X)
print(y)
print(coef)
for i in range(len(y)): plt.scatter(X[i], y[i])
plt.show()

# Add outlier data
np.random.seed(0)
X[:n_outliers] = 3 + 0.5 * np.random.normal(size=(n_outliers, 1))
y[:n_outliers] = -3 + 10 * np.random.normal(size=n_outliers)

# Fit line using all data
lr = linear_model.LinearRegression()
lr.fit(X, y)

# Robustly fit linear model with RANSAC algorithm
ransac = linear_model.RANSACRegressor()
ransac.fit(X, y)
inlier_mask = ransac.inlier_mask_
outlier_mask = np.logical_not(inlier_mask)

# Predict data of estimated models
line_X = np.arange(min(X), max(X))[:, np.newaxis]
line_y = lr.predict(line_X)
line_y_ransac = ransac.predict(line_X)

# Compare estimated coefficients
print("Estimated coefficients (true, linear regression, RANSAC):")
print(coef, lr.coef_, ransac.estimator_.coef_)

print(inlier_mask)
print(outlier_mask)

lw = 2
plt.scatter(X[inlier_mask], y[inlier_mask], color='yellowgreen', marker='.',
            label='Inliers')
plt.scatter(X[outlier_mask], y[outlier_mask], color='gold', marker='.',
            label='Outliers')
plt.plot(line_X, line_y, color='navy', linewidth=lw, label='Linear regressor')
plt.plot(line_X, line_y_ransac, color='cornflowerblue', linewidth=lw,
         label='RANSAC regressor')
plt.legend(loc='lower right')
plt.xlabel("Input")
plt.ylabel("Response")
plt.show()
