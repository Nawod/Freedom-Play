import cv2
import time
from time import sleep
import numpy as np
import HandTrackingModule as htm
import math

#libraries for volume control
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#libraries for brightness control
import screen_brightness_control as sbc

#libraires for control media player
import pyautogui
import win32api

import vlc


wCam, hCam = 640, 480 #define the camera width and height
pTime = 0
volBar = 400
briBar = 400
area = 0
recColor = (0,255,0)

#Define the web camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

#create an objector for hand tracking module
detector = htm.handDetector(detectionCon=0.85, maxHands=1)

#pycaw audio control libray
#https://github.com/AndreMiras/pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

volPer = int(volume.GetMasterVolumeLevelScalar()*100)
briPer = sbc.get_brightness()

while True:
    success, img = cap.read()
    Fimg = cv2.flip(img, 1) #flip the image

    Fimg = detector.findHands(Fimg) #call htm method to detect hand
    lmList, bBox = detector.findPosition(Fimg) #Getting landmark list
    
    if len(lmList) !=0:
        #filter and define the hand size
        area = (bBox[2]-bBox[0]) * (bBox[3]-bBox[1])//100
        # print(area)

        #check which fingers uped
        fingers = detector.fingersUp()
        # print(fingers)

# Volume control
        #voulum control using thumb and index fingers. Volume value set using middle finger
        #check weather only realted fingers uped
        if fingers[3] == 0 and fingers[4] == 0 and fingers[1] ==1:
            #hand size between 400 & 1300
            if 400<area<1300:
                # recColor = (0,255,0)
                #calculate distance between thumb and index finger
                Fimg, length,  info = detector.findDistance(Fimg, 4, 8)

                #convert tip lentgh range into volume range
                volBar = np.interp(length,[30,270],[400, 150])
                volPer = np.interp(length,[30,270],[0, 101])

                #Reduce the resolution
                smoothness = 5
                volPer = smoothness * round(volPer/smoothness)

                #set the voulme when the middle finger is up
                if fingers[2]==1:
                    # volume.SetMasterVolumeLevel(vol, None)
                    volume.SetMasterVolumeLevelScalar(volPer/100, None)
                    cv2.circle(Fimg, (info[4],info[5]), 10, (255,0,255), cv2.FILLED)

            #hand size between 150 & 400
            if 150<area<400:
                # recColor = (255,0,0)
                #calculate distance between thumb and index finger
                Fimg, length,  info = detector.findDistance(Fimg, 4, 8)

                #convert tip lentgh range into volume range
                volBar = np.interp(length,[10,160],[400, 150])
                volPer = np.interp(length,[10,160],[0, 101])

                #Reduce the resolution
                smoothness = 5
                volPer = smoothness * round(volPer/smoothness)

                #set the voulme when the middle finger is up
                if fingers[2]==1:
                    # volume.SetMasterVolumeLevel(vol, None)
                    volume.SetMasterVolumeLevelScalar(volPer/100, None)
                    cv2.circle(Fimg, (info[4],info[5]), 10, (255,0,255), cv2.FILLED)

            #hand size between 20 & 150
            if 20<area<150:
                # recColor = (255,0,0)
                #calculate distance between thumb and index finger
                Fimg, length,  info = detector.findDistance(Fimg, 4, 8)

                #convert tip lentgh range into volume range
                volBar = np.interp(length,[5,80],[400, 150])
                volPer = np.interp(length,[5,80],[0, 101])

                #Reduce the resolution
                smoothness = 5
                volPer = smoothness * round(volPer/smoothness) 

                #set the voulme when the middle finger is up
                if fingers[2]==1:
                    # volume.SetMasterVolumeLevel(vol, None)
                    volume.SetMasterVolumeLevelScalar(volPer/100, None)
                    cv2.circle(Fimg, (info[4],info[5]), 10, (255,0,255), cv2.FILLED)
            
            #display sound range
            cv2.rectangle(Fimg, (50,150), (85,400), recColor, 3)
            cv2.rectangle(Fimg, (50,(int(volBar))), (85,400), recColor, cv2.FILLED)
            cv2.putText(Fimg, f'{int(volPer)}%', (40,450), cv2.FONT_HERSHEY_PLAIN , 2, recColor, 2)

# Brightness control
        #brightness control using pinky finger. brightness value set using thumb finger
        #check weather only realted fingers uped
        if fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0:
            #hand size between 400 & 1300
            if 500<area<1200:
                # recColor = (0,255,0)
                #calculate distance between wrist and pinky finger tip
                Fimg, length,  info = detector.findDistance(Fimg, 0, 20)

                #convert tip lentgh range into brightness range
                briBar = np.interp(length,[100,360],[400, 150])
                briPer = np.interp(length,[100,360],[0, 100])

                #Reduce the resolution
                smoothness = 5
                briPer = smoothness * round(briPer/smoothness)

                #set the brightness when the thumb finger is up
                if fingers[0]==1:
                    sbc.set_brightness(briPer)
                    cv2.circle(Fimg, (info[4],info[5]), 10, (255,0,255), cv2.FILLED)

            if 150<area<500:
                # recColor = (255,0,0)
                #calculate distance between wrist and pinky finger tip
                Fimg, length,  info = detector.findDistance(Fimg,  0, 20)

                #convert tip lentgh range into volume range
                briBar = np.interp(length,[60,220],[400, 150])
                briPer = np.interp(length,[60,220],[0, 100])

                #Reduce the resolution
                smoothness = 5
                briPer = smoothness * round(briPer/smoothness)

                #set the brightness when the thumb finger is up
                if fingers[0]==1:
                    sbc.set_brightness(briPer)
                    cv2.circle(Fimg, (info[4],info[5]), 10, (255,0,255), cv2.FILLED)

            #hand size between 20 & 150
            if 20<area<150:
                # recColor = (255,0,0)
                #calculate distance between wrist and pinky finger tip
                Fimg, length,  info = detector.findDistance(Fimg,  0, 20)
                # print(int(length))

                #convert tip lentgh range into volume range
                briBar = np.interp(length,[25,85],[400, 150])
                briPer = np.interp(length,[25,85],[0, 100])

                #Reduce the resolution
                smoothness = 5
                briPer = smoothness * round(briPer/smoothness)  

                #set the brightness when the thumb finger is up
                if fingers[0]==1:
                    sbc.set_brightness(briPer)
                    cv2.circle(Fimg, (info[4],info[5]), 10, (255,0,255), cv2.FILLED)


            #display brightness
            cv2.rectangle(Fimg, (50,150), (85,400), (0,255,255), 3)
            cv2.rectangle(Fimg, (50,(int(briBar))), (85,400), (0,255,255), cv2.FILLED)
            cv2.putText(Fimg, f'{int(briPer)}%', (40,450), cv2.FONT_HERSHEY_PLAIN , 2, (0,255,255), 2)

# Media play/paush control
        #check weather the all fingers are uped
        #media play/pause when hand is opened
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and fingers[0] == 1:
            VK_MEDIA_PLAY_PAUSE = 0xB3
            hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)
            win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode)
            sleep(2)


    cVol = int(volume.GetMasterVolumeLevelScalar()*100)
    cv2.putText(Fimg, f'Set Vol: {int(cVol)}', (400,40), cv2.FONT_HERSHEY_PLAIN , 2, (0,255,0), 2)

    cBri = int(sbc.get_brightness())
    cv2.putText(Fimg, f'Set Bright: {int(cBri)}', (400,80), cv2.FONT_HERSHEY_PLAIN , 2, (0,255,255), 2)

    #calculate the fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(Fimg, f'FPS: {int(fps)}', (10,40), cv2.FONT_HERSHEY_PLAIN , 2, (255,0,255), 2)

    #visualized the output
    # cv2.imshow("Img", Fimg)
    cv2.waitKey(1)