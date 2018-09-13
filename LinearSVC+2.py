import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from matplotlib import style
style.use("ggplot")

#Use Numpy for array. Use capital "X". These are our features
X = np.array([[1,2],
             [5,8],
             [1.5,1.8],
             [8,8],
             [1,0.6],
             [9,11]])

#You label the pairs
y = [0,1,0,1,0,1]

#Classifier using support vector machine (svm). Where C = dummy for machine learning
clf = svm.SVC(kernel='linear', C = 1.0)

#We fit the array into features
clf.fit(X,y)

#Now we are ready to use machine learning to predict
print(clf.predict([[10.58,10.76]]))

#Classify data using coeficients
w = clf.coef_[0]
print(w)

#Algorithm for line creation
a = -w[0] / w[1]

#We can use the max and min values of our features
xx = np.linspace(0,12)
yy = a * xx - clf.intercept_[0] / w[1]

#Ploting, using "k" for black and "-" for line
h0 = plt.plot(xx, yy, 'k-', label="non weighted div")

#Graphing using Numpy. X, then 0 element, actually the x in the array, 1st element is actually the y, or the second element in the array, C for color
plt.scatter(X[:, 0], X[:, 1], c = y)

plt.legend()
plt.show()



