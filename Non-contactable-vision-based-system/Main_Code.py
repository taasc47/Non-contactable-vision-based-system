

#importing libraries
import cv2 
import numpy as np


image0 = cv2.imread("num0.jpeg",1)
image1 = cv2.imread("num1.jpeg",1)
image2 = cv2.imread("num2.jpeg",1)
image3 = cv2.imread("num3.jpeg",1)
image4 = cv2.imread("num4.jpeg",1)
image5 = cv2.imread("num5.jpeg",1)
image6 = cv2.imread("num6.jpeg",1)
image7 = cv2.imread("num7.jpeg",1)
image8 = cv2.imread("num8.jpeg",1)
image9 = cv2.imread("num9.jpeg",1)
image_pr=cv2.imread("precntg.jpeg",1)



def num1(x):    #for the first digit of the level display
    if x==100:
        return image_pr
    if x==1:
        return image1
    if x==2:
        return image2
    if x==3:
        return image3
    if x==4:
        return image4
    if x==5:
        return image5
    if x==6:
        return image6
    if x==7:
        return image7
    if x==8:
        return image8
    if x==9:
        return image9
    if x==0:
        return image0
def num2(y):    #For the second digit of the level display
    if y==1:
        return image1
    if y==2:
        return image2
    if y==3:
        return image3
    if y==4:
        return image4
    if y==5:
        return image5
    if y==6:
        return image6
    if y==7:
        return image7
    if y==8:
        return image8
    if y==9:
        return image9
    if y==0:
        return image0
    

video= cv2.VideoCapture(0)  #captured by front camera(0)
video.set(3,640)    #width
video.set(4,480)    #height
video.set(10,140)  #brigtness


a=0
refArea=29000   # Area is taken as pixels for fully-filled bottle

ref=np.ones((414,126,3),np.uint8)   #to join the display with main images


while(video.isOpened()):
    check, frame = video.read()     #reading video frame
    hvs = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    #frame is converted to hsv image
    
    lower_blue = np.array([2,136,70])       #HSV values for the selected fluid color is applied
    upper_blue = np.array([24,255,255])
    
    mask =cv2.inRange(hvs, lower_blue, upper_blue)  # black & white mask is created to track the object
    
    _,contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) #contours are found on that mask
    
    mask2 = cv2.bitwise_and(frame,frame, mask=mask)     #convert B&W mask to filter the selected on the white area
    
    hor_join = np.hstack((frame,mask2))     # mask2 and frame are jointed horizontally(matrix joint)
    
    
    
    
    
    
    a=np.count_nonzero(mask==255)   # cross sectional area is counted pixel-vise
    #print(a)
    
    if a<refArea:
        #print(a,"refArea")
        a=a/refArea
        a=a*100
        a=int(a)
        a=str(a)    # precentage of instantaneous area over referenced area(fully-filled) 
        
        if len(a)==1: # for areas of 0 to 9 (for displaying 1 index)
        
            i=int(a[0])
        
        
            h_join = np.hstack((num2(0),num1(i),num1(100))) #first index,second index, precentage sign of display
            vjoin = np.vstack((h_join,ref))                 #vetically joined with the ref arrays
            hjoin = np.hstack((vjoin,hor_join))             #horizontally joined with main captures
            
            cv2.imshow("full",hjoin)
            print(a+"%")        #precentage is shown in the console
        
        else:
            
            if int(a)>80:               # After 80% contour should applied
                for contour in contours:
                    area = cv2.contourArea(contour)
        
                    if area > 20000 and area< 30000:
                       cv2.drawContours(hor_join, contours, -1, (0, 0, 255), 3)
                
                i=int(a[1]) #there are two index to display on the counter now
                j=int(a[0])
        
                h_join = np.hstack((num2(j),num1(i),num1(100)))
                vjoin = np.vstack((h_join,ref))
                hjoin = np.hstack((vjoin,hor_join)) # joined same as before
                
                cv2.imshow("full",hjoin)
                print(a+"%")
            else:               # for precentages less than 80%
                i=int(a[1])
                j=int(a[0])
        
                h_join = np.hstack((num2(j),num1(i),num1(100)))
                vjoin = np.vstack((h_join,ref))
                hjoin = np.hstack((vjoin,hor_join))
                
                cv2.imshow("full",hjoin)
                print(a+"%")
    
   
    
    key= cv2.waitKey(1) #when q button is pushed the windows close. 
    if key == ord('q'):
        break

video.release()


cv2.destroyAllWindows()



