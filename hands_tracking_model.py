import cv2
import mediapipe as mp
from firebase import firebase
from knn import KNN_model
from knn import KNNDataBase
import importlib


class HandTrackingModel:
    def __init__(self):
        self.handsModel = mp.solutions.hands             
        self.hands = self.handsModel.Hands(min_tracking_confidence=0.2)        
        self.mpDraw = mp.solutions.drawing_utils        
        self.markStyle = self.mpDraw.DrawingSpec(color=(0,255,0),thickness=5)
        self.connectionStyle = self.mpDraw.DrawingSpec(color=(255,255,255),thickness=2)
        self.relativeLocationArray = []
        self.isRelativeRecording = False
        self.dataModel = importlib.import_module('knn.KNNDataBase')
        self.knnModel = KNN_model.KnnModel(dataModel=self.dataModel)
        self.retrieveData = 0
        self.fireBaseURL = 'https://cube-bddd3-default-rtdb.asia-southeast1.firebasedatabase.app/'
        self.fireBase = firebase.FirebaseApplication(self.fireBaseURL,None)



    def updateImage(self,image):
        self.image = image
        self.imageWidth = self.image.shape[1]
        self.imageHeight = self.image.shape[0]
        self.processImage()
        return self.image

    def processImage(self):
        rgbImage=cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB) 
        result=self.hands.process(rgbImage)
        self.traverseHandsMarks(result)

    def identifyRightHand(self,handMark):
        indexFingerMark = handMark.landmark[12]
        wristMark = handMark.landmark[0]
        if indexFingerMark.x -wristMark.x > 0:
            return True
        else:
            return False
        
    def getNodeRelativeLocation(self,handMarks):
        tempArray = []
        handMarksArray = []
        wristMark = handMarks.landmark[0]
        for i,landMark in enumerate(handMarks.landmark):
            if i == 0:
                continue
            relativeX = int( (landMark.x - wristMark.x) * self.imageWidth)
            relativeY = int( (landMark.y - wristMark.y) * self.imageHeight)

            if(handMarks.landmark[12].x - wristMark.x > 0):
                tempArray.append(f'left{i}')
            else:
                tempArray.append(f'right{i}')

            tempArray.append(relativeX)
            tempArray.append(relativeY)
            handMarksArray.append(tempArray)
            self.relativeLocationArray.append(tempArray)
            tempArray = []

    def drawHandsMarks(self,handMarks):
        self.mpDraw.draw_landmarks(self.image, handMarks, self.handsModel.HAND_CONNECTIONS, self.markStyle,self.connectionStyle)
    def drawHandsMarksInfo(self,node,x,y):    
        cv2.putText(self.image,str(node),(x-25,y+5),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,0,255),2) 

    def drawHandsPredictResult(self,result,x,y):
        x = int(x * self.imageWidth)
        y = int(y * self.imageHeight)
        cv2.putText(self.image,str(result),(x,y-40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),1) 

    def drawRetrieveDataCount(self):
        cv2.putText(self.image,str(self.retrieveData),(100,100),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),1) 

    def processListForKnn(self,inputList):
        wrist = inputList[0]
        del inputList[0]
        for i in inputList:
            i[1] = i[1] - wrist[1]
            i[2] = i[2] - wrist[2]   
            del i[0]  
        return inputList
    def enterMarkInfo(self,isRight,x,y):
        outputList = []
        if(isRight == True):
            outputList.append('right')
        else:
            outputList.append('left')
        outputList.append(x)
        outputList.append(y)
        return outputList
    
    def updateMovementToServer(self,currentMove):
        self.fireBase.put('','currentMove',currentMove)
    
    def traverseHandsMarks(self,result):
        handMarkInfoList = []
        self.drawRetrieveDataCount()
        if result.multi_hand_landmarks:
            for handMarks in result.multi_hand_landmarks:
                self.drawHandsMarks(handMarks)
                knnArray = []
                for i,landMark in enumerate(handMarks.landmark):
                    xPosition = int( landMark.x * self.imageWidth)
                    yPosition = int( landMark.y * self.imageHeight)
                    zPosition = int( landMark.z * 10000)
                    isRightHand = self.identifyRightHand(handMarks) #Ture->right

                    handMarkInfoList.append(self.enterMarkInfo(isRightHand,xPosition,yPosition))
                    
                    self.drawHandsMarksInfo(i,xPosition,yPosition)
                

                knnArray = self.processListForKnn(handMarkInfoList)
           
                if(isRightHand):
                    predictResult = self.knnModel.predictRightHand(knnArray) 
                    self.drawHandsPredictResult(predictResult,handMarks.landmark[12].x,handMarks.landmark[12].y)
                else:
                    predictResult = self.knnModel.predictLeftHand(knnArray)
                
                self.updateMovementToServer(predictResult)
                handMarkInfoList = []
                knnArray = []
                        
                
                if(self.isRelativeRecording):
                    #print("============")
                    self.getNodeRelativeLocation(handMarks)
                   # print(self.relativeLocationArray)

            if ( self.isRelativeRecording == True ):
                self.retrieveData = self.retrieveData + 1
                #print(f"Retreve : {self.retrieveData}")
                self.isRelativeRecording = False
                    
         