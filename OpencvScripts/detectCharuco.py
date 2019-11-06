import numpy as np
import cv2
import cv2.aruco as aruco
mtx = np.array([
        [964.65,       0, 527.526],
        [      0, 962.454, 358.1611],
        [      0,       0,       1],
        ])
dist = np.array( [-1.25332777e-01, 1.07327000e+00, -1.52290760e-03, 1.76339938e-03, -2.57610603e+00] )
cap = cv2.VideoCapture(0)
aruco_dict = aruco.Dictionary_get(aruco.DICT_APRILTAG_36H11)
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, 
                                                          aruco_dict, 
                                                          parameters=parameters)
    if ids is not None:
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.136, mtx, dist) 
        diamondConrners,diamondIds = cv2.aruco.detectCharucoDiamond(frame,corners,ids,2,cameraMatrix=mtx,distCoeffs=dist)
        retval,rvec1,tvec1=cv2.aruco.estimatePoseCharucoBoard(diamondConrners,diamondIds,frame,mtx,dist)
        cv2.imshow(frame)
        print(tvec)
        cv2.waitKey(0)
        cv2.destroyAllWindows()