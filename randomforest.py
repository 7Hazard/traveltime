from traintest import *

# random forest regression
from sklearn.ensemble import RandomForestRegressor

# maxScore = 0
# maxDepth = 1
# maxEstimators = 1

# for x in range(1, 14):
#   for y in range(1, 60):
#     regr = RandomForestRegressor(max_depth=x, n_estimators=y, random_state=0)
#     regr.fit(x_train, y_train)
#     score = regr.score(x_test, y_test)
#     if score > maxScore:
#       maxScore = score
#       maxDepth = x
#       maxEstimators = y

# print(f"{maxDepth}: {maxScore}")

regr = RandomForestRegressor(max_depth=3, n_estimators=10, random_state=0)
regr.fit(x_train, y_train)
score = regr.score(x_test, y_test)
print(f"{score}")
