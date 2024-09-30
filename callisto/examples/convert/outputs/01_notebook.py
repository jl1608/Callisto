import pandas
import xgboost
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt 

# global properties
seed = 42
test_size = 0.2

# load data
data = pandas.read_csv('iris.csv', header=None)
data.columns = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']

dataset = data.values
# split data into X and y
X = dataset[:,0:4]
Y = dataset[:,4]

data

# plot a chart
plt.plot(dataset[:,0], "r--") 
plt.show()
plt.savefig("./outputs/sepal-length-plot.png")

# encode string class values as integers
label_encoder = LabelEncoder()
label_encoder = label_encoder.fit(Y)
label_encoded_y = label_encoder.transform(Y)

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, label_encoded_y, test_size=test_size, random_state=seed)
# fit model no training data
model = xgboost.XGBClassifier()
model.fit(X_train, y_train)
print(model)

# make predictions for test data
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]

# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))
with open("./outputs/metrics.txt", "w+") as f:
    f.write("Accuracy: %.2f%%" % (accuracy * 100.0))

