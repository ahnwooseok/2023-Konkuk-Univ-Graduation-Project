import matplotlib.pyplot as plot
import numpy as np
import math

x = np.random.rand(100,1)
x = x * 10-5

y = np.array([math.sin(i) for i in x])
#평균 0 표준편차 1인 가우시안 정규 분포 
y = y + np.random.randn(100)
#서포트 백터 머신 모듈 가져오기 
from sklearn.svm import SVR
model = SVR()
model.fit(x,y)
relation_square = model.score(x, y)
print('결정계수 R :', relation_square)
y_p = model.predict(x)

plot.scatter(x, y, marker = '+')
plot.scatter(x, y_p, marker = 'o')
plot.show()