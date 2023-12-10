from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import importlib

class KnnModel:
    def __init__(self,dataModel):
        self.scaler = StandardScaler()
        self.knnClassifier = KNeighborsClassifier(n_neighbors=7)
        self.KnnModelDataBase = dataModel

    def predictSingleNode(self,inputData):
        newDataScaled = self.scaler.transform(inputData) #標準化輸入資料
        prediction = self.knnClassifier.predict(newDataScaled)
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
        finalPredictResult = max(resultList,key=resultList.count)
        return finalPredictResult

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
        finalPredictResult = max(resultList,key=resultList.count)
        return finalPredictResult
# knnModel = KnnModel()
# knnModel.predictLeftHand([[24, -32],[63, -50],[101, -49],[131, -43],[53, -69],[94, -77],[125, -72],[149, -64],[40, -45],[90, -51],[166, 47],[24, -32],[24, -32],[24, -32],[24, -32],[24, -32],[24, -32],[24, -32],[24, -32],[24, -32],])
# knnModel.predictRightHand([[24, -32],[63, -50],[101, -49],[131, -43],[53, -69],[94, -77],[125, -72],[149, -64],[40, -45],[90, -51],[166, 47],[24, -32],[24, -32],[24, -32],[24, -32],[24, -32],[24, -32],[24, -32],[24, -32],[24, -32],])