## 導入Python數據處理套件
import numpy as np
import pandas as pd
## 導入繪圖套件
import matplotlib.pyplot as plt
## 導入迴歸模型套件
from sklearn.linear_model import LinearRegression
## 導入多項式套件，建構多項式迴歸模型所需的套件
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
## 導入區分訓練集與測試集套件
from sklearn.model_selection import train_test_split

## 創建數據集
xList = [1,2,7,8,18,26,28,32,35,37,39,41,44,50,58]
yList = [28000, 46000, 56000, 68000, 62000, 74000, 60000, 85000, 98000, 80000, 86000, 93000, 170000,200000, 280000]
# learning_hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# salary = [0,1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169,196, 255]

## 組合成DataFrame格式
data_dict = {'X': xList, 'Y': yList}
df = pd.DataFrame(data_dict)
## X = pd.DataFrame(df.iloc[:,0])
## y = pd.DataFrame(df.iloc[:,1])
X = df[['X']]
y = df[['Y']]
print(X)
print('=============')
print(y)


## 訓練不同次方多項式的迴歸模型

## 裝不同次方多項式的分數
scores = []





## 訓練多項式迴歸模型
regressor = make_pipeline(PolynomialFeatures(4), LinearRegression())
regressor.fit(X,y)
## 裝進精準度分數的陣列
scores.append(regressor.score(X,y))
## 視覺化多項式迴歸模型線

coefficients = regressor.named_steps['linearregression'].coef_
intercept = regressor.named_steps['linearregression'].intercept_


print("coefficients:", coefficients)
print("intercept:", intercept)

coefficients1=float(coefficients[0][0])
coefficients2=float(coefficients[0][1])
coefficients3=float(coefficients[0][2])
coefficients4=float(coefficients[0][3])
intercept1 = float(intercept[0])

#回歸出的曲線為 y=X*coefficients1+X^2*coefficients2+X^3*coefficients3+intercept

# X*coefficients1+X^2*coefficients2+X^3*coefficients3+intercept
# Y=X*coefficients1+X^2*coefficients2+X^3*coefficients3+intercept
# print(X)
plt.plot(X,regressor.predict(X), label = 'Polynomial Degree 2' )

# print("16:"+regressor.predict(16))
input = 5
print(intercept)
print((input * coefficients2)+((input ** 2) * coefficients3)+((input ** 3)* coefficients4 )+intercept)
print(' Score: ' + str(scores[0])) 
## 繪製數據集資料點
#plt.scatter(X,y)
plt.legend()
plt.show()


## 印出分數
# for i in range(len(scores)):
#   print('Polynomial Degree ' + str(i+1) + ' Score: ' + str(scores[i]))

