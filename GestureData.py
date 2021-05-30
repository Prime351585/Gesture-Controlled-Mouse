# Gesture Control in Photo Album

import cv2
import mediapipe as mp
import time

class handDetector():

    def __init__(self,mode=False,maxHands=1,DetectionConf=0.5,TrackConf=0.5):

        self.mode=mode
        self.maxHands=maxHands
        self.DetectionConf=DetectionConf
        self.TrackConf=TrackConf   
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands,self.DetectionConf,self.TrackConf)
        self.mpDraw=mp.solutions.drawing_utils
        
     
    def findHands(self,img,draw=True):
        
        imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)       
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img ,handLms,self.mpHands.HAND_CONNECTIONS)

        return img

    def findPos(self,img):

        lmList=[]

        if self.results.multi_hand_landmarks:
            Hand=self.results.multi_hand_landmarks[0]
            for id,ln in enumerate(Hand.landmark):
                h,w,c=img.shape
                cx,cy=int(w*ln.x),int(h*ln.y)
                lmList.append((id,cx,cy))

        return lmList


def main(Width,Height):
    
    pTime=0
    cTime=0
    cap=cv2.VideoCapture(0)
    cap.set(3,Width)
    cap.set(4,Height)
    detector=handDetector()

    while True:
            success,img=cap.read()
            img=detector.findHands(img)
            List=detector.findPos(img)
            if len(List)!=0 :
                cv2.circle(img,(List[4][1],List[4][2]),5,(255,194,0),10)   # For Test Purpose only 
                # print(List[4])
            cTime=time.time()
            FPS=1/(cTime-pTime)
            pTime=cTime
            cv2.putText(img,str(int(FPS)),(10,70),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,255),1)
            cv2.imshow("Image",img)
            if cv2.waitKey(1) & 0xff == ord('j'):
                break

if __name__ == "__main__":
    main(800,600)

# //////////////////////////////////////////////////////////////////////////////// Made By Harsh Maurya.......With 💖 



