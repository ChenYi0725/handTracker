import cv2
import mediapipe as mp
import recorder as r


class HandTrackingModel:
    def __init__(self):
        self.handsModel = mp.solutions.hands             
        self.hands = self.handsModel.Hands(min_tracking_confidence=0.2)        
        self.mpDraw = mp.solutions.drawing_utils        
        self.markStyle = self.mpDraw.DrawingSpec(color=(0,255,0),thickness=5)
        self.connectionStyle = self.mpDraw.DrawingSpec(color=(255,255,255),thickness=2)
        self.recorder = r.Recorder()

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

    def drawHandsMarks(self,handMarks):
        self.mpDraw.draw_landmarks(self.image, handMarks, self.handsModel.HAND_CONNECTIONS, self.markStyle,self.connectionStyle)
    def numberHandsMarks(self,node,x,y):
        cv2.putText(self.image,str(node+1),(x-25,y+5),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,0,255),2) 



    def traverseHandsMarks(self,result):
        if result.multi_hand_landmarks:
            for handMarks in result.multi_hand_landmarks:
                self.drawHandsMarks(handMarks)
                for i,landMark in enumerate(handMarks.landmark):
                    xPosition = int( landMark.x * self.imageWidth)
                    yPosition = int( landMark.y * self.imageHeight)
                    zPosition = int( landMark.z * 10000)
                    isRightHand = self.identifyRightHand(handMarks)
                    self.numberHandsMarks(i,xPosition,yPosition)
                    self.recorder.record(i+1,xPosition,yPosition,zPosition,isRightHand,self.image)

                   
         