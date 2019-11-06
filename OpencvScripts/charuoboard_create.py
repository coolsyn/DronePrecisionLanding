import numpy as np
import cv2
import cv2.aruco as aruco
#img=np.random.random((200,200))
size=3
aruco_dict = aruco.Dictionary_get(aruco.DICT_APRILTAG_36H11)
board = cv2.aruco.CharucoBoard_create(size,size,.025,.0125,aruco_dict)
img = board.draw((200*size,200*size))
cv2.imshow('charuco',img)
cv2.waitKey(0)
cv2.destroyAllWindows()