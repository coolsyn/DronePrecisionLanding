import cv2 
import cv2.aruco as aruco
import numpy as np

#相机标定矩阵
mtx = np.array([
        [964.65,       0, 527.526],
        [      0, 962.454, 358.1611],
        [      0,       0,       1],
        ])
dist = np.array( [-1.25332777e-01, 1.07327000e+00, -1.52290760e-03, 1.76339938e-03, -2.57610603e+00] )

cap = cv2.VideoCapture(0)#捕获视频
font = cv2.FONT_HERSHEY_SIMPLEX #字体
pi=3.1415926
while True:  
    ret, frame = cap.read()   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    aruco_dict = aruco.Dictionary_get(aruco.DICT_APRILTAG_36H11)
    parameters =  aruco.DetectorParameters_create()  
      
    #lists of ids and the corners beloning to each id  
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, 
                                                          aruco_dict, 
                                                          parameters=parameters)  
  
#    if ids != None: 
    if ids is not None:
          
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.136, mtx, dist) 
        # Estimate pose of each marker and return the values rvet and tvec---different 
        # from camera coeficcients  
        (rvec-tvec).any() # get rid of that nasty numpy value array error  
        #print("tecv:"+str(tvec))
        degree=rvec*180/pi
        print("recv:"+str(degree))

#        aruco.drawAxis(frame, mtx, dist, rvec, tvec, 0.1) #Draw Axis  
#        aruco.drawDetectedMarkers(frame, corners) #Draw A square around the markers
        
        for i in range(rvec.shape[0]):
            aruco.drawAxis(frame, mtx, dist, rvec[i, :, :], tvec[i, :, :], 0.03)
            aruco.drawDetectedMarkers(frame, corners, ids)
  
  
  
    else:  
        ##### DRAW "NO IDS" #####  
        cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)  
  
    # Display the resulting frame  
    cv2.imshow("frame",frame)  
    
    key = cv2.waitKey(1)
    
    if key == 27:         # 按esc键退出
        print('esc break...')  
        cap.release()
        cv2.destroyAllWindows()
        break
    
    if key == ord(' '):   # 按空格键保存
#        num = num + 1
#        filename = "frames_%s.jpg" % num  # 保存一张图像
        filename = str(time.time())[:10] + ".jpg"  
        cv2.imwrite(filename, frame)
