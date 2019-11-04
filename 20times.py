import numpy as np
import cv2
import cv2.aruco as aruco
color=[255,255,255]
font = cv2.FONT_HERSHEY_SIMPLEX
aruco_dict = aruco.Dictionary_get(aruco.DICT_APRILTAG_36H11)
img = np.random.random((200,200))
for i in range(25):
    img=aruco.drawMarker(aruco_dict, i, 200, img, 1)
    img_bor=cv2.copyMakeBorder(img,200,200,200,200,cv2.BORDER_CONSTANT,value=color)
    text='id:'+str(i)
    img_bor=cv2.putText(img_bor,text,(280,500),font,1,(0,0,0),2)
    fileDir='/Users/sunyunong/Downloads/Arucotags/'+str(i)+'.jpg'
    cv2.imshow("imgbor",img_bor)
    cv2.imwrite(fileDir,img_bor)
cv2.waitKey(0)
cv2.destroyAllWindows()