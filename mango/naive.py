import pandas as pd
import warnings
warnings.filterwarnings('ignore')
 
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
 
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = [iris.target_names[x] for x in iris.target]
 
X = df.drop('species', axis=1)
y = df['species']
 
clf = GaussianNB().fit(X,y)
print(clf.predict(X)[:3]) 
print(clf.get_params()) ## GaussianNB 클래스 인자 설정 정보
print('정확도 : ', clf.score(X,y)* 100 ,'%') ## 성능 평가 점수(Accuracy)

