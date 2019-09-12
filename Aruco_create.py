
import numpy as np
import cv2
import cv2.aruco as aruco
 
# 选择aruco模块中预定义的字典来创建一个字典对象
# 这个字典是由250个marker组成的，每个marker的大小为5*5bits
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
img = np.random.random((200,200))
# marker的图像可以使用drawMarker()函数生成。
# 第一个参数是之前创建的字典对象。
# 第二个参数是marker的id，在这个例子中选择的是字典DICT_6X6_250第23个marker。
# 第三个参数，200，是输出Marker图像的大小。在这个例子中，输出的图像将是200x200像素大小。为了避免变形，这一参数最好和位数+边界的大小成正比。
# 第四个参数是输出的图像。
# 最后一个参数是一个可选的参数，它指定了Marer黑色边界的大小。这一大小与位数数目成正比。例如，值为2意味着边界的宽度将会是2的倍数。默认的值为1。
img=aruco.drawMarker(aruco_dict, 3, 200, img, 1)
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()