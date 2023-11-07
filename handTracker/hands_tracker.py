import camera
import hands_tracking_model as hm
import cv2
import camera 


class HandTracker:
    def __init__(self) -> None:
        self.handTrackingModel = hm.HandTrackingModel()
        self.imageCatcher =  camera.Camera()
       

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
        print(self.handTrackingModel.recorder.sortData())
        #print(self.handTrackingModel.recorder.recordedDictionary)


