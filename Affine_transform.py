import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
def a(img,coordinates):

    h,w,_=img.shape
    
    # Locate points of the documents
    # or object which you want to transform
    pts1 = np.float32([coordinates[0],coordinates[1],coordinates[2],coordinates[3]])
    pts2 = np.float32([[0, 0], [w, 0],
                       [w, h], [0, h]])
    
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
        #input two kinds of arrays and ret
        # urn the M matrix - the twist matrix
    result = cv2.warpPerspective(img, matrix,(w,h))
     
    # Wrap the transformed image

    # cv2.imshow('frame', img) # Initial Capture
    # cv2.imshow('frame1', result) # Transformed Capture
    # cv2.waitKey(0)
    # img_resized=cv2.resize(result,crop_size)
    return result
import os
for file in os.listdir("Plate_data"):
    label_0,label_1,label_2,label_3=0,0,0,0
    if 'jpg' not in file:continue
    img=cv2.imread("Plate_data/"+file)
    h,w,_=img.shape
    
    h_img,w_img,_=img.shape
    labels=['top_left','top_right',"bot_right","bot_left"]
    txt=open("Affine_test/results/"+file.replace('jpg','txt'),"r").read().splitlines()
    coors=[0,0,0,0]
    num_label=0
    x_full,y_full=[],[]
    for line in txt:
        
        label,x,y,w,h,_=[float(i) for i in line.split()]
        x=x*2*w_img
        h,w,y=h*h_img,w*w_img,y*2*h_img
        if label!=4:
            #img=cv2.circle(img,(int(x/2),int(y/2)),5,(255,255,0),-5)
            coors[int(label)]=[int(x/2),int(y/2)]
            x_full.append(int(x/2))
            y_full.append(int(y/2))
            
            if label==1 and label_1 !=1:label_1+=1
            if label==2 and label_2 !=1:label_2+=1
            if label==3 and label_3 !=1:label_3+=1
            if label==0 and label_0 !=1:label_0+=1
    num_label=label_0+label_1+label_2+label_3
    if num_label!=4:continue
        #x_min,x_max,y_min,y_max=int((x-w)/2),int((x+w)/2),int((y-h)/2),int((y+h)/2)
        # cv2.rectangle(img,(x_min,y_min),(x_max,y_max),(0,255,0),1)
    x_min,y_min,x_max,y_max=min(x_full),min(y_full),max(x_full),max(y_full)
    crop_img=img[ y_min:y_max,x_min:x_max,:]   
    for i,box in enumerate(coors):
        coors[i]=[ box[0]-x_min,box[1]-y_min ]
        crop_img=cv2.circle(crop_img,( box[0]-x_min,box[1]-y_min ),5,(255,255,0),-5)
    
    cv2.imshow("A",crop_img)
    cv2.waitKey(0)

    # cv2.imwrite("Affine_test/results/new.jpg",img)
    # cv2.imshow("A",crop_img)
    # cv2.waitKey(0)
    # cv2.imwrite("Affine_test/newdata494_new.jpg",crop_img)
    h,w,_=crop_img.shape

    img_resized=a(crop_img,coors)
    h,w,_=img_resized.shape

    # cv2.imshow("Resize",img_resized)
    # cv2.waitKey(0)
    print(file)
    cv2.imwrite('Affine_test/crop_plate/'+file,img_resized)
