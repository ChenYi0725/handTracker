import camera
import hands_tracking_model as hm
import cv2
import camera 
import trail_maker as tm


class HandTracker:
    def __init__(self) -> None:
        self.handTrackingModel = hm.HandTrackingModel()
        self.imageCatcher =  camera.Camera()
        self.trailMaker = tm.TrailMaker()

    def onMouse(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.handTrackingModel.recorder.isRecording = True

    def start(self): 
        while True:
            isFrameCaptured,image = self.imageCatcher.getImage()
            if not isFrameCaptured:
                break
            image = self.handTrackingModel.updateImage(image)
            cv2.imshow("Hands Detection", image)   
            cv2.setMouseCallback("Hands Detection",self.onMouse) #滑鼠事件
            if cv2.waitKey(1) == ord('q'):      #按下q關閉
                break 
        self.showData()
    
    def showData(self):
        dataList = self.handTrackingModel.recorder.sortDataForRegression()
        xList = self.handTrackingModel.recorder.getCertainIndexData(index=1,allDataList=dataList)
        yList = self.handTrackingModel.recorder.getCertainIndexData(index=2,allDataList=dataList)
        # print("x:")
        # print(xList)
        # print("=======")
        # print("y:")
        # print(yList)
        for i in range(-21,22):
            if i == 0:      #遇0跳過
                continue
            print(i)
            # print(xList[i])
            self.makeTrail(xList=xList[i],yList=yList[i])    
        #從-21->21
    
    def makeTrail(self,xList,yList):
        self.trailMaker.enterList(xList,yList)
        self.trailMaker.start()

