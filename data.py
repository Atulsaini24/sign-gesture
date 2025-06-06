import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

cap = cv2.VideoCapture(0) #zero is id no. for our web cam
offset = 20
imgSize = 300
detector = HandDetector(maxHands=1) #1 for just single hand

folder = "Data/C"
counter = 0

while True:
    success, img = cap.read()
    if not success:
        continue
        
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize,imgSize,3), np.uint8)*255 #255 is white colour no.     
        # Make sure the coordinates are within the image bounds
        imgHeight, imgWidth = img.shape[:2]
        x = max(0, x)
        y = max(0, y)
        w = min(w, imgWidth - x)
        h = min(h, imgHeight - y)

        if w > 0 and h > 0:
            imgCrop = img[y-offset:y + h+offset, x-offset:x + w+offset]
            
            imgCropShape = imgCrop.shape
            
            aspectRatio = h/w
            if aspectRatio >1:
                k = imgSize/h
                wCal = math.ceil(k*w)
                imgResize = cv2.resize(imgCrop,(wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize-wCal)/2)
                imgWhite[:, wGap:wCal+wGap] = imgResize
            
            else:
                k = imgSize/w
                hCal = math.ceil(k*h)
                imgResize = cv2.resize(imgCrop,(imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize-hCal)/2)
                imgWhite[hGap:hCal+hGap, :] = imgResize

            cv2.imshow("ImageCrop", imgCrop)#output for hand crop
            cv2.imshow("ImageWhite", imgWhite)#output for hand background
            
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    if key & 0xFF == ord('s'):
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(counter)
cap.release()
cv2.destroyAllWindows()

