import cv2
import numpy as np
import os
import argparse
parser = argparse.ArgumentParser(description="Semi-Supervised Semantic Segmentation")
parser.add_argument("--file", type=str, default="images.txt")
parser.add_argument("--output_folder", type=str, default="crop_retina")

def Perspective_Trans(img, coordinates):
        # ?[xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]]
        h,w,_=img.shape
        # Locate points of the documents
        # or object which you want to transform
        pts1 = np.float32([coordinates[0],coordinates[2], coordinates[3], coordinates[1]])
        pts2 = np.float32([[0, 0], [w, 0],
                        [w, h], [0, h]])
        
        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
            #input two kinds of arrays and ret
            # urn the M matrix - the twist matrix
        result = cv2.warpPerspective(img, matrix,(w,h))
        
        # Wrap the transformed image
        # img_resized=cv2.resize(result,crop_size)
        return result
def main():
    args = parser.parse_args()
    with open(args.file,'r') as f1:
        list_files = f1.read().splitlines()
        for file in list_files:
            file_txt=file.split('/')[-1].replace('jpg','txt')
            txt=open('licenseplate_evaluate/licenseplate_txt/'+file_txt,"r").read().splitlines()
            print(file)
            img=cv2.imread(file)
            img=cv2.resize(img, (224,224))
            txt = [txt[0]]
            print(txt)
            for line in txt:
                x1, y1, x2, y2, x3, y3, x4, y4=[int(float(i)) for i in line.split()]
            xmin, ymin=min(x1, x2, x3, x4),min(y1, y2, y3, y4)
            xmax, ymax=max(x1, x2, x3, x4),max(y1, y2, y3, y4)
                #found bounding box contain all of them.

            crop_img=img[ int(ymin)-5:int(ymax)+5,int(xmin)-5:int(xmax)+5,:]  
                #expand a little bit  
            coors= [ [x1, y1],[x2, y2],[x3, y3],[x4,y4]]
            coors.sort()
            for i,box in enumerate(coors):
                coors[i] = [ int(box[0]-(int(xmin)-5)),int(box[1]-(int(ymin)-5)) ]
            
            img_resized = Perspective_Trans(crop_img, coors)
            # cv2.imshow("Resize",img_resized)
            # cv2.waitKey(0)
            cv2.imwrite(f"{args.output_folder}/abc.jpg", img_resized)

if __name__ == "__main__":
    main()