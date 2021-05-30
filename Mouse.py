#  Main Program

import cv2
import mediapipe as mp
import time
import GestureData as Gd
import numpy as np
import pyautogui 
import autopy

i=0
LHpt=8
pTime=0
cTime=0
cap=cv2.VideoCapture(0)
Width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)

Height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
RectDim=125
cap.set(3,Width)
cap.set(4,Height)
detector=Gd.handDetector()

scale=autopy.screen.size()
L1 = RectDim
L2 = RectDim
L3 = int(Width - RectDim)
L4 = int(Height - RectDim  )

Smoothing = 4

Xc,Yc = 0,0

Xp,Yp = 0,0

j=20

while True:

        success,img=cap.read()
        img=detector.findHands(img)
        List=detector.findPos(img)
        cv2.rectangle(img,(L1  ,L2  ),(L3  ,L4 ),(255,0,255),3)

        cv2.circle(img,(RectDim,RectDim),2,(255,255,255),2)
        cv2.circle(img,(int(Width)-RectDim,int(Height)-RectDim),2,(0,0,255),2)
        cv2.circle(img,(RectDim,int(Height)-RectDim),2,(0,255,0),2)
        cv2.circle(img,(int(Width)-RectDim,RectDim),2,(255,0,0),2)

        if len(List)!=0 :

            if  List[8][1]  > L1 and List[8][1]  < L3  and List[8][2]  >  L2  and  List[8][2]  < L4:

                X = List[8][1]

                Y = List[8][2]

                Xs = (X - L1) * ( scale[0] ) / ( L3 - L1)

                Ys = (Y - L2) * ( scale[1] ) / ( L4 - L2) 

                Xc = Xp + (Xs - Xp)/Smoothing

                Yc = Yp + (Ys - Yp)/Smoothing

                # print( X , Y , Xs , Ys )
                autopy.mouse.move( Xc , Yc )

                Xp=Xc

                Yp=Yc

                cv2.circle(img,(int((List[6][1]+List[5][1])/2),int((List[6][2]+List[5][2])/2)),3,(255,120,0),3)

                cv2.line(img,(List[4][1],List[4][2]),(int((List[6][1]+List[5][1])/2),int((List[6][2]+List[5][2])/2)),(255,0,0),3)
                
                Length=np.sqrt((List[4][1]-int((List[6][1]+List[5][1])/2))**2  +  (List[4][2] - int((List[6][2]+List[5][2])/2))**2) 

                cv2.circle(img,(List[8][1],List[8][2]),3,(255,120,0),3)

                cv2.line(img, (List[4][1], List[4][2]), (List[8][1], List[8][2]), (0, 0, 255), 3)
                
                Length1 = np.sqrt((List[4][1] - List[8][1]) ** 2 + (List[4][2] - List[8][2]) ** 2)
            
                if Length < 25  :
 
                    pyautogui.rightClick()

                if Length1 < 25 :
           
                    autopy.mouse.click()

        cTime = time.time()
        FPS = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(FPS)), (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 1)
        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xff == ord('j') :
            
            break

# //////////////////////////////////////////////////////////////////////////////// Made By Harsh Maurya.......With 💖 
