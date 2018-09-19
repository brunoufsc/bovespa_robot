import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

import pandas as pd
from matplotlib import style
style.use("ggplot")

def Build_Data_Set(features = ["DE Ratio",
                               "Trailing P/E"]):
    data_df = pd.DataFrame.from_csv("key_stats.csv")

    data_df = data_df[:100]

    #X is coordinate. Use capital X. The y is target, or classification.
    #Data_df features is to consider these two columns with DE Ratio and Trailing P/E, bring their value to a Python list
    X = np.array(data_df[features].values)#.tolist())

    #Pandas allow to replace previous definitions with numbers
    y = (data_df["Status"]
         .replace("underperform",0)
         .replace("outperform",1)
         .values.tolist())


    return X,y

#Defining Numpy Machine Learning Analysis Parameters
def Analysis():
    X, y = Build_Data_Set()

    clf = svm.SVC(kernel="linear", C= 1.0)
    clf.fit(X,y)

    #Graph the analysis
    w = clf.coef_[0]
    a = -w[0] / w[1]
    xx = np.linspace(min(X[:, 0]), max(X[:, 0]))
    yy = a * xx - clf.intercept_[0] / w[1]

    h0 = plt.plot(xx,yy, "k-", label="non weighted")

    #This is a shotcut code to get the first element 0, and second element 1, of the array of data
    #C=y is use color yellow to differentiate plots
    plt.scatter(X[:, 0],X[:, 1],c=y)
    plt.ylabel("Trailing P/E")
    plt.xlabel("DE Ratio")
    plt.legend()

    plt.show()



Analysis()
