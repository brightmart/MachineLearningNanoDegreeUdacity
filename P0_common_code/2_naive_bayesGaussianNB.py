import numpy as np
X=np.array([[-1,-1],[-2,-1],[-3,-2],[1,1],[2,1],[3,2]])
Y=np.array([1,1,1,2,2,2])
from sklearn.naive_bayes import GaussianNB
clf=GaussianNB()
clf.fit(X,Y)
labelPredicted=clf.predict([[-0.8,-1]])
print labelPredicted


def NBAccuracy(features_train, labels_train, features_test, labels_test):
    """ compute the accuracy of your Naive Bayes classifier """
    ### import the sklearn module for GaussianNB
    from sklearn.naive_bayes import GaussianNB

    ### create classifier
    clf =GaussianNB()

    ### fit the classifier on the training features and labels
    clf.fit(features_train,labels_train)

    ### use the trained classifier to predict labels for the test features
    pred =clf.predict(features_test)


    ### calculate and return the accuracy on the test data
    ### this is slightly different than the example, 
    ### where we just print the accuracy
    ### you might need to import an sklearn module
    import numpy as ny
    accuracy = ny.mean(pred==labels_test) #1
	accuracy=clf.score(features_test, labels_test)  #2
	from sklearn.metrics import accuracy_score
	accuracy=accuracy_score(pred, labels_test) #3
    print accuracy
    return accuracy