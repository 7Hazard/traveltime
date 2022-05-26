from traintest import *

# linear regression
from sklearn import linear_model

reg = linear_model.LinearRegression()
reg.fit(x_train, y_train)
score = reg.score(x_test, y_test)
print(f"{score}")
