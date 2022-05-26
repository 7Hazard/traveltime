import trips
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(
    trips.x,
    trips.y,
    test_size=0.26,
    random_state=6
)

