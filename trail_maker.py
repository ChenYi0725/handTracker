import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

class TrailMaker:
    def __init__(self):
        self.totalDataList = []
        
    
    def enterList(self,xList,yList):
        self.xList = xList
        self.yList = yList
        self.dataFrame = pd.DataFrame({'X': self.xList, 'Y': self.yList})
        self.xColumn = self.dataFrame[['X']]
        self.yColumn = self.dataFrame[['Y']]
        

    def tarinModed(self):
        self.regressor = make_pipeline(PolynomialFeatures(4), LinearRegression())
        self.regressor.fit(self.xColumn,self.yColumn)

    def getCoefficients(self):
        coefficients = self.regressor.named_steps['linearregression'].coef_[0]
        return coefficients
        

    def getIntercept(self):
        intercept = self.regressor.named_steps['linearregression'].intercept_
        return intercept
    # def getDelta(self):
    
    def start(self):
        self.tarinModed()
        # print(self.getCoefficients())
        self.totalDataList.append(self.getCoefficients().tolist())
        print(self.totalDataList)       #-21~21