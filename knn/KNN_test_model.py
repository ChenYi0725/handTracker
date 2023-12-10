from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
# import KNN_model_database as db
import importlib

KNN_model_database = importlib.import_module('KNN_model_database')
k1Accuracy = []
k2Accuracy = []
k3Accuracy = []
k4Accuracy = []
k5Accuracy = []
k6Accuracy = []
k7Accuracy = []
k8Accuracy = []
k9Accuracy = []
k10Accuracy = []
k11Accuracy = []
k12Accuracy = []
k13Accuracy = []
k14Accuracy = []
k15Accuracy = []
k16Accuracy = []
k17Accuracy = []
k18Accuracy = []
k19Accuracy = []
k20Accuracy = []
for j in range(1,21):
    # 將資料集分為訓練集和測試集

    dataList = getattr(KNN_model_database,f'left{j}Data',None)
    
    labelList = getattr(KNN_model_database,f'left{j}Label',None)

    trainData, testData, trainLabel, testLabel = train_test_split(dataList, labelList, test_size=0.2, random_state=42)
    # 標準化特徵值
    scaler = StandardScaler()
    trainData = scaler.fit_transform(trainData)
    testData = scaler.transform(testData)

    for i in range(1,21):       #找出最適合K值
        # 創建 KNN 分類器，指定 k 值
        knnClassifier = KNeighborsClassifier(n_neighbors = i)
        # 在訓練集上擬合模型
        knnClassifier.fit(trainData, trainLabel)
        # 使用模型進行預測
        yPredictic = knnClassifier.predict(testData)
        # 計算準確率
        accuracy = accuracy_score(testLabel, yPredictic)
        print(f'left node{j} k= {i} accuracy: {accuracy}')
        locals()[f"k{j}Accuracy"].append(accuracy)
        print(yPredictic)
    print()
print("================================================================")
for j in range(1,21):
    # 將資料集分為訓練集和測試集

    dataList = getattr(KNN_model_database,f'right{j}Data',None)
    
    labelList = getattr(KNN_model_database,f'right{j}Label',None)

    trainData, testData, trainLabel, testLabel = train_test_split(dataList, labelList, test_size=0.2, random_state=42)
    # 標準化特徵值
    scaler = StandardScaler()
    trainData = scaler.fit_transform(trainData)
    testData = scaler.transform(testData)

    for i in range(1,21):       #找出最適合K值
        # 創建 KNN 分類器，指定 k 值
        knnClassifier = KNeighborsClassifier(n_neighbors = i)
        # 在訓練集上擬合模型
        knnClassifier.fit(trainData, trainLabel)
        # 使用模型進行預測
        yPredictic = knnClassifier.predict(testData)
        # 計算準確率
        accuracy = accuracy_score(testLabel, yPredictic)
        print(f'right node{j} k= {i} accuracy: {accuracy}')
        locals()[f"k{j}Accuracy"].append(accuracy)
    print()

for i in range(1,21):
   averge = sum(locals()[f"k{i}Accuracy"]) / len(locals()[f"k{i}Accuracy"])
   print(f'k{i}Accuracy Averge:{averge}')
print(f'testData : {testData}')
#    print(locals()[f"k{i}Accuracy"])
#=========================================================================================
# K = 7
