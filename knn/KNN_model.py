from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import importlib


# dataModel = importlib.import_module('KNNDataBase')

# print("[")
# for i in range(1,21):
#     dataList = getattr(dataModel,f'right{i}Data',None)
#     labelList = getattr(dataModel,f'right{i}Label',None)    
#     print(f'{dataList[-1]},')
# print("]")


class KnnModel:
    def __init__(self,dataModel):
        self.scaler = Normalizer()
        self.knnClassifier = KNeighborsClassifier(n_neighbors=7)
        self.KnnModelDataBase = dataModel

    def predictSingleNode(self,inputData):
        scaledData = self.scaler.transform(inputData) #標準化輸入資料
        prediction = self.knnClassifier.predict(scaledData)
        return prediction

    def predictLeftHand(self,handNodeList):
        resultList = []
        for i in range(1,21):
            dataList = getattr(self.KnnModelDataBase,f'left{i}Data',None)
            labelList = getattr(self.KnnModelDataBase,f'left{i}Label',None)
            #標準化
            dataList = self.scaler.fit_transform(dataList)
            #創建模型
            self.knnClassifier.fit(dataList, labelList)
            # print(handNodeList)
            singlePredictResult = self.predictSingleNode([handNodeList[i-1]])
            resultList.append(singlePredictResult)
        # for i in range(5):
        #     del resultList[0]   

        finalPredictResult = max(resultList,key=resultList.count)
        return finalPredictResult[0]

    def predictRightHand(self,handNodeList):
        resultList = []
        for i in range(1,21):
            dataList = getattr(self.KnnModelDataBase,f'right{i}Data',None)
            labelList = getattr(self.KnnModelDataBase,f'right{i}Label',None)
            #標準化
            dataList = self.scaler.fit_transform(dataList)
            #創建模型
            self.knnClassifier.fit(dataList, labelList)
            # print(handNodeList)
            singlePredictResult = self.predictSingleNode([handNodeList[i-1]])
            resultList.append(singlePredictResult)
        # for i in range(5):
            # del resultList[0] 
        finalPredictResult = max(resultList,key=resultList.count)
        # print(resultList)
        return finalPredictResult[0]

mydownlist = [
[-24, -28],
[-55, -48],
[-90, -47],
[-116, -41],
[-40, -61],
[-82, -74],
[-116, -68],
[-142, -59],
[-28, -35],
[-82, -42],
[-125, -38],
[-157, -32],
[-25, -4],
[-82, -3],
[-126, -1],
[-157, 5],
[-31, 28],
[-84, 29],
[-118, 24],
[-143, 21],
]
# myleftlist = [[ -21, -26], [ -48, -47], [ -74, -55], [ -94, -55], [ -38, -64], [ -59, -81], [ -83, -80], [ -104, -75], [ -28, -45], [ -67, -49], [ -100, -46], [ -125, -42], [ -23, -20], [ -64, -20], [ -95, -19], [ -118, -17], [ -24, 5], [ -64, 3], [ -89, 1], [ -110, 0]]
# knnModel = KnnModel(importlib.import_module('KNNDataBase'))
# print(knnModel.predictRightHand(mydownlist))
