import time
import cv2
class Recorder:
    def __init__(self):
        self.isRecording:bool = False
        self.recordedDictionary:list = []
        self.neededFrame = 25
        self.handQuantity = 2
        self.nodeQuantity = 21
        self.sortedData = []
        self.recordTimes = 0
        self.recordedFrame = 0
       
    
    def startRecord(self):
        self.isRecording = True        
    
    def drawRecordingMark(image):
        cv2.circle(image,(image.shape[1]-30,30),radius=10,color=(0,0,255),thickness=-1) #劃出錄影標示

    def record(self,node,x,y,z,isRight,image):
        dataTargetQuantity=self.neededFrame*self.handQuantity*self.nodeQuantity
        if self.isRecording:
            cv2.circle(image,(image.shape[1]-30,30),radius=10,color=(0,0,255),thickness=-1) #劃出錄影標示
            if isRight:
                leftOrRight:str = 'Right'
            else:
                leftOrRight:str = 'Left'

            if self.recordedFrame<dataTargetQuantity:
                self.recordedFrame = self.recordedFrame+1
                recordedDatum:dict = {'node':node,'x':x,'y':y,'z':z,'leftOrRight':leftOrRight,'recordedtimes':self.recordTimes}
                self.recordedDictionary.append(recordedDatum)
            else:
                self.recordedFrame = 0
                self.isRecording = False
                self.recordTimes = self.recordTimes + 1
                print("recorded once")
        else:
            pass
    
    def calculateDelta(self):
        isFirstData = True
        
        for i in range(len(self.recordedDictionary)):  #新增資料
            for j in range(i):
                if((self.recordedDictionary[i-(j+1)]['node']==self.recordedDictionary[i]['node'])and(self.recordedDictionary[i-(j+1)]['leftOrRight']==self.recordedDictionary[i]['leftOrRight']) ):
                    self.recordedDictionary[i]['deltaX']=self.recordedDictionary[i]['x']-self.recordedDictionary[i-(j+1)]['x']
                    self.recordedDictionary[i]['deltaY']=self.recordedDictionary[i]['y']-self.recordedDictionary[i-(j+1)]['y']
                    self.recordedDictionary[i]['deltaZ']=self.recordedDictionary[i]['z']-self.recordedDictionary[i-(j+1)]['z']
                    isFirstData=False
                    break
            if(isFirstData):
                self.recordedDictionary[i]['deltaX']=0
                self.recordedDictionary[i]['deltaY']=0
                self.recordedDictionary[i]['deltaZ']=0   

    def seperateToLeftAndRight(self,outputList):
        leftHandData = []
        rightHandData = []
        for item in self.recordedDictionary:           
            if item['leftOrRight'] == 'Left':
                leftHandData.append(item)
            elif item['leftOrRight'] == 'Right':
                rightHandData.append(item)

        for i in rightHandData:             #將右手的節點改為負號
            i['node']= -i['node']

        outputList.append(leftHandData)
        outputList.append(rightHandData)
        return outputList

    def turnToNeededData(self,allDataList):
        outputList=[]
        for i in allDataList:
            data = [[d['node'],d['deltaX'], d['deltaY'],d['deltaZ']] for d in i]
            outputList.append(data)
        return outputList

    def sortData(self):
        outputDataList=[]

        self.calculateDelta()
        outputDataList = self.seperateToLeftAndRight(outputDataList)
        outputDataList = self.turnToNeededData(outputDataList)

        return outputDataList


