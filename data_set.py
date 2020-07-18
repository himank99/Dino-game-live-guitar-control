import numpy as np
from sklearn.model_selection import train_test_split
data = np.loadtxt('Desktop/dino/pcp.data', delimiter=',') # load the data
X = data[:,:12]
Y = data[:,12]
m=data.shape[0]
Y = Y.astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
y_train = y_train.reshape((-1,1))
y_test = y_test.reshape((-1,1))
