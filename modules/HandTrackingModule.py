import cv2
import mediapipe as mp
import time
import math

class handDetector():
    #Detection model initialization
    def __init__(self, mode=False, maxHands = 2, modelCom = 1, detectionCon = 0.5, trackCon=0.5 ):
        # static_image_mode = False,
        # max_num_hands = 2,
        # model_complexity = 1,
        # min_detection_confidence = 0.5,
        # min_tracking_confidence = 0.5

        self.mode = mode
        self.maxHands = maxHands
        self.modelCom = modelCom
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands #Mediapipe hand detection
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.modelCom,self.detectionCon,self.trackCon) #create an object for detect hands
        self.mpDraw = mp.solutions.drawing_utils #object for draw hand landmarks

        self.tipIds = [4, 8, 12, 16, 20]

    #hand detector method
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convert image to RGB
        self.results = self.hands.process(imgRGB) #call hands object

        #retrived and visualized hands info
        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                #Check weather draw is True
                if draw:
                    self.mpDraw.draw_landmarks(img, handLMS, self.mpHands.HAND_CONNECTIONS) #visualized the hand landmarks

        return img
                

    #land mark position values extract
    def findPosition(self, img, handNo=0, draw=True):
        xList = [] #all x values
        yList = [] #all y values
        bBox = [] #bounding box values
        self.lmList = [] #landmark list
        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
             
            for id, lm in enumerate(myHand.landmark): #landmarks details/locations
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h) #position according to display pixles
                
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id,cx, cy])                  

            #create bounding box
            xMin, xMax = min(xList), max(xList)
            yMin, yMax = min(yList), max(yList)
            bBox = xMin, yMin, xMax, yMax

            if draw:
                cv2.rectangle(img, (bBox[0]-20, bBox[1]-20),(bBox[2]+20, bBox[3]+20), (0,255,0), 2)

        return self.lmList , bBox

    #detect uped fingers
    def fingersUp(self):
        fingers = []
        #thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        #4 fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers
    
    #find distance between landmarks
    def findDistance(self,img, p1, p2, draw=True):

        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2 #center of the tips
        length = math.hypot(x2-x1, y2-y1)
        
        if draw:
            cv2.circle(img, (x1,y1), 15, (0,255,0), cv2.FILLED) #draw circle
            cv2.circle(img, (x2,y2), 15, (0,255,0), cv2.FILLED)
            cv2.line(img, (x1,y1),(x2,y2), (255,0,0), 3) #draw a line between tip points
            cv2.circle(img, (cx,cy), 10, (0,255,0), cv2.FILLED)

        return img, length, [x1,y1,x2,y2,cx,cy]

def main():
    #define the webcam
    cap = cv2.VideoCapture(0)

    detector = handDetector() #call hand detector class

    pTime = 0 #varibles for calculate FPS
    cTime = 0

    while True:
        success, img = cap.read()
        img = detector.findHands(img) #call the method
        lmList = detector.findPosition(img)
        
        if len(lmList) !=0: #check weather any hand detected
            print(lmList[4])

        #Calculate the FPS
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN , 3, (255,0,255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    

if __name__ == "__main__":
    main()