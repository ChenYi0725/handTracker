import cv2
import time

class Camera:
    def __init__(self) :
        self.isCameraOn = True
        self.capturedFrame = cv2.VideoCapture(0)         ##內部攝影機的編號為0
        self.capturedFrame.set(cv2.CAP_PROP_FPS, 30)     ##設定攝影機的FPS
        self.previousTime = 0

    def getFps(self,image):          
        fps= 1/(time.time()-self.previousTime)
        self.previousTime = time.time()   
        cv2.putText(image, f"fps : {int(fps)}",(30,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),1) 
        return image
    
    def getImageInfo(self,image):
        self.imageHeight = image.shape[0]
        self.imageWidth = image.shape[1]

    def setImageHud(self,image):
        self.getImageInfo(image)
        image=self.getFps(image)
        return image
    
    def getImage(self):
        isSecreenCaptured, image = self.capturedFrame.read()  
        image = self.setImageHud(image)
        if isSecreenCaptured:
            return isSecreenCaptured,image
        
