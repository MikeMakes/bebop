import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_red = np.array([0,120,70]) #example value
    upper_red = np.array([10,255,255]) #example value

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

     # calculate moments of binary image
    M = cv2.moments(mask)
    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)#Convertimos la imagen diff a escala de grises
    blur =cv2.GaussianBlur(gray, (5,5), 0)#Aplicamos un filtro de desenfoque gaussiano
    _, thresh =cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY)#Aplicamos un umbral básico o binario
    dilated = cv2.dilate(thresh, None, iterations=3)#Aplicamos operacion morfologica de dilatado
    contours, _=cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#Definimos los contornos
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 300:
            continue
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Pelota: {}".format('Roja'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # put text and highlight the center
    cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(frame, "Pelota Roja", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',gray)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()