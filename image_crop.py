""" 
Calculate the distance from each color and find the shortest one
"""

import cv2
import numpy as np
import pandas as pd

cropping = False

x_start, y_start, x_end, y_end = 0, 0, 0, 0

image = cv2.imread(r'./000000113282.jpg')
oriImage = image.copy()
imgWidth = oriImage.shape[1] - 40

index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv("./colors.csv", header=None, names=index)

r = g = b = xpos = ypos = 0
def getRGBvalue(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    xpos = x
    ypos = y
    b,g,r = img[y,x]
    b = int(b)
    g = int(g)
    r = int(r)
    
    
def colorname(B,G,R):
    minimum = 10000
    for i in range(len(df)):
        d = abs(B-int(df.loc[i,"B"])) + abs(G-int(df.loc[i,"G"])) + abs(R-int(df.loc[i,"R"]))
        if (d<=minimum):
            minimum = d
            cname = df.loc[i,"color_name"] + "Hex" + df.loc[i, "hex"]
    return cname

def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping

    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True

    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y

    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False # cropping is finished

        refPoint = [(x_start, y_start), (x_end, y_end)]

        if len(refPoint) == 2: #when two points were found
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            b,g,r = image[y,x]
            b = int(b)
            g = int(g)
            r = int(r)
            cv2.rectangle(image, (20,20), (imgWidth, 60),(b,g,r), -1)
            text = colorname(b,g,r) + '   R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
            cv2.putText(image,text, (50,50),2, 0.8, (255,255,255),2,cv2.LINE_AA)    
            if(r+g+b >= 600):
                cv2.putText(image,text,(50,50), 2, 0.8, (0,0,0),2,cv2.LINE_AA)   
            cv2.imshow("Cropped", image)


cv2.namedWindow("Display")
cv2.setMouseCallback("Display", mouse_crop)

while True:

    i = oriImage.copy()

    if not cropping:
        cv2.imshow("Display", oriImage)

    elif cropping:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow("Display", i)
    if cv2.waitKey(20) & 0xFF == 27:
        break

    cv2.waitKey(1)

# close all open windows
cv2.destroyAllWindows()