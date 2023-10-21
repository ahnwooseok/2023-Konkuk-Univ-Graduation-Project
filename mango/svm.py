from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split  
import pandas as pd
from sklearn.svm import SVC  
from sklearn.metrics import classification_report, confusion_matrix  

iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.DataFrame({'class':iris.target})
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)  

svclassifier = SVC(kernel='linear', degree=8)  
svclassifier.fit(X_train, y_train) 

y_pred = svclassifier.predict(X_test)  
print('score : ',svclassifier.score(X_test,y_test))
print(confusion_matrix(y_test, y_pred))  
print(classification_report(y_test, y_pred)) 

