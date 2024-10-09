import os
import numpy as np

import math
import time
import cv2

def padding(img,bbox):

    # read image

    old_image_height, old_image_width, channels = img.shape

    # create new image of desired size and color (blue) for padding
    new_image_width = 600
    new_image_height = 600
    color = (0,0,0)
    result = np.full((new_image_height,new_image_width, channels), color, dtype=np.uint8)
    # compute center offset
    x_center = (new_image_width - old_image_width) // 2
    y_center = (new_image_height - old_image_height) // 2
    # copy img image into center of result image
    result[y_center:y_center+old_image_height, 
        x_center:x_center+old_image_width] = img
    new_bb=[]
    return result
def remove_blank(img):
    remove_x=0
    remove_y=0
    total=(img[:,:,0])
    total_blank=[]
    for i in range(img.shape[0]):
        blank=True
        count=0
        for j in range(img.shape[1]):
            if total[j][i]==0:
                count+=1
        if count!=img.shape[1]:
            blank=False
        total_blank.append(blank)
        
            
    first_blank=total_blank.index(False)
    remove_y=first_blank
    total_blank.reverse()
    last_blank=len(total_blank)-1-total_blank.index(False)
    img=img[first_blank:last_blank,:,:]
    #cv2.imshow("A",img)
    #cv2.waitKey(0)

    total=(img[:,:,0])
    total_blank=[]
    for i in range(img.shape[1]):
        blank=True
        count=0
        for j in range(img.shape[0]):
            if total[j][i]==0:
                count+=1
        if count!=img.shape[0]:
            blank=False
        total_blank.append(blank)
        
            
    first_blank=total_blank.index(False)
    remove_x=first_blank
    total_blank.reverse()
    last_blank=len(total_blank)-1-total_blank.index(False)
    img=img[:,first_blank:last_blank,:]
    #cv2.imshow("A",img)
    #cv2.waitKey(0)

    return img,[remove_x,remove_y]

def product(x_min,y_min,image,angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  ini=np.array([x_min,y_min,1])
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  return [int(i) for i in np.dot(rot_mat,ini)]

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result
for choice in range(1,3):
    for i in range(6):
        for file in os.listdir("Plate_data"):
            if choice==1:
                #left
                angle=np.random.randint(i*5,i*5+5)
            else:
                angle=np.random.randint(i*5+330,i*5+5+330)
            if "txt"  in file or  "trans" in file  :
                continue
            angle=9
            name=file.replace("jpg","txt")
            new_name=name.split(".txt")[0]+"_trans_"+str(angle)+".txt"
            img=cv2.imread("Plate_data/"+file)
            tem_h,tem_w,_=img.shape
            if tem_h>600 or tem_w>600:
                continue

            #print(file)
            data=open("Plate_data/"+name,"r")
            data=data.read().splitlines()
            h_img,w_img,_=img.shape
            bbox=[]
            # for id,line in enumerate(data):
            #         label,x,y,w,h=[ float(i) for i in line.split()]
            #         w,h,x,y=w*w_img,h_img*h,x*w_img*2,y*h_img*2

            #         x_min,x_max=int((x-w)/2),int((x+w)/2)
            #         y_min,y_max=int((y-h)/2),int((y+h)/2)
   
            #         cv2.rectangle(img,(x_min,y_min),(x_max,y_max),(0,0,255))

            b=rotate_image(img,angle)
            cv2.imshow("B",b)
            cv2.waitKey(0)
            tem_img=b.copy()
            total_labels=[]
            for id,line in enumerate(data):
                    label,x,y,w,h=[ float(i) for i in line.split()]
                    w,h,x,y=w*w_img,h_img*h,x*w_img*2,y*h_img*2

                    x_min,x_max=int((x-w)/2),int((x+w)/2)
                    y_min,y_max=int((y-h)/2),int((y+h)/2)
                    x_min,y_min=product(x_min,y_min,img,angle)
                    x_max,y_max=product(x_max,y_max,img,angle)

                    bbox.append([x_min,y_min,x_max,y_max])
                    total_labels.append(label)
                    cv2.rectangle(b,(x_min,y_min),(x_max,y_max),(0,0,255))
            cv2.imshow("B",b)
            cv2.waitKey(0)
            bbox=[]
            for id,line in enumerate(data):
                    label,x,y,w,h=[ float(i) for i in line.split()]
                    w,h,x,y=w*w_img,h_img*h,x*w_img*2,y*h_img*2

                    x_min,x_max=int((x-w)/2),int((x+w)/2)
                    y_min,y_max=int((y-h)/2),int((y+h)/2)
                    bot_left=product(x_min,y_min,tem_img,angle)
                    top_right=product(x_max,y_max,tem_img,angle)
                    bot_right=product(x_max,y_min,tem_img,angle)
                    top_left=product(x_min,y_max,tem_img,angle)

                    pts=np.array([bot_left,bot_right,top_right,top_left],np.int32)
                    pts = pts.reshape((-1, 1, 2))

                    tem_img = cv2.polylines(tem_img, [pts],True, (0,0,255), 2)
                    bbox.append([bot_left,bot_right,top_right,top_left])
                    cv2.rectangle(b,(x_min,y_min),(x_max,y_max),(0,0,255))
            cv2.imshow("Tem Img",tem_img)
            cv2.waitKey(0)

            img=padding(img,bbox)
            new_h,new_w,_=img.shape
            x_cen=(new_w-w_img)//2
            y_cen=(new_h-h_img)//2
            img=rotate_image(img,angle)
            img,remove=remove_blank(img)
            new_bbox=[]
            bounding_boxes=[]
            for box in bbox:
                each_box=[]
                x_min,y_min=1000,1000
                x_max,y_max=0,0
                for coor in box:
                    x,y=coor
                    x+=x_cen-remove[0]
                    y+=y_cen-remove[1]
                    x_min=min(x_min,x)
                    x_max=max(x_max,x)
                    y_min=min(y_min,y)
                    y_max=max(y_max,y)
                    each_box.append([x,y])
                new_bbox.append(each_box)

                #x_min,y_min=product(x_min,y_min,img,angle)
                #x_max,y_max=product(x_max,y_max,img,angle)
                pts=np.array(each_box,np.int32)
                pts = pts.reshape((-1, 1, 2))
                bounding_boxes.append([x_min,y_min,x_max,y_max])
            #    img = cv2.polylines(img, [pts],True, (0,0,255), 2)
            cv2.imwrite("augment_plates/"+new_name.replace("txt","jpg"),img)
            new_h,new_w,_=img.shape
            with open("augment_plates/"+new_name,"w") as f:
                for i,box in enumerate(bounding_boxes):
                    x_min,y_min,x_max,y_max=box
                    if angle<=10:
                        pass
                    elif angle<=20:
                        x_min+=2
                        y_max-=2
                        x_max-=2
                    else:
                        x_min+=3
                        y_max-=3
                        y_min+=2
                        x_max-=2
                    if angle>=350:
                        y_max+=2
                    elif angle>=340:
                        y_max+=2
                        x_min+=2
                    else:
                        y_max+=2
                        y_min+=2
                        x_min+=2
                    cv2.rectangle(img,(x_min,y_min),(x_max,y_max),(0,0,255))
                    x_cen=(x_min+x_max)/(2*new_w)
                    y_cen=(y_max+y_min)/(2*new_h)
                    w=(x_max-x_min)/(new_w)
                    h=(y_max-y_min)/new_h
                    line=[int(total_labels[i]),x_cen,y_cen,w,h]
                    f.write(" ".join(str(i) for i in line))
                    f.write("\n")
            #print(file)
                    cv2.rectangle(img,(x_min,y_min),(x_max,y_max),(0,255,0))
            cv2.imshow("A",img)
            cv2.waitKey(0)


