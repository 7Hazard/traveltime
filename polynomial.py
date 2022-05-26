from traintest import *

# polynomial regression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

# maxDegree = 1
# maxScore = 0

# for x in range(1, 8):
#   poly = PolynomialFeatures(degree=x)
#   px_train = poly.fit_transform(x_train)
#   px_test = poly.fit_transform(x_test)

#   reg = linear_model.LinearRegression()
#   reg.fit(px_train, y_train)
#   score = reg.score(px_test, y_test)

#   if score > maxScore:
#     maxScore = score
#     maxDegree = x

# print(f"{maxDegree}: {maxScore}")

poly = PolynomialFeatures(degree=3)
px_train = poly.fit_transform(x_train)
px_test = poly.fit_transform(x_test)

reg = linear_model.LinearRegression()
reg.fit(px_train, y_train)
score = reg.score(px_test, y_test)
print(f"{score}")
