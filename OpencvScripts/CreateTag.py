import PIL.Image as Image
import os
import numpy as np
import cv2
import cv2.aruco as aruco
#导入库
#生成多个tag文件
color=[255,255,255]#边框颜色为白色
font = cv2.FONT_HERSHEY_SIMPLEX#设置字体
aruco_dict = aruco.Dictionary_get(aruco.DICT_APRILTAG_36H11)#字典为AprilTag
img = np.random.random((200,200))#设置图片大小
for i in range(25):#生成id：0-24的图片
    img=aruco.drawMarker(aruco_dict, i, 200, img, 1)#生成图片
    img_bor=cv2.copyMakeBorder(img,200,200,200,200,cv2.BORDER_CONSTANT,value=color)#生成边框
    text='id:'+str(i)#添加文本字符串
    img_bor=cv2.putText(img_bor,text,(280,500),font,1,(0,0,0),2)#添加文本
    FilePath='/Users/sunyunong/Downloads/Arucotags/'+str(i)+'.jpg'#文件路径
    cv2.imwrite(fileDir,img_bor)#保存文件
cv2.waitKey(1)
cv2.destroyAllWindows()

#拼接tags文件
IMAGES_PATH = '/Users/sunyunong/Downloads/Arucotags/' # 图片集地址
IMAGES_FORMAT = ['.jpg', '.JPG'] # 图片格式
IMAGE_SIZE = 240 # 每张小图片的大小
IMAGE_ROW = 5 # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 5 # 图片间隔，也就是合并成一张图后，一共有几列
IMAGE_SAVE_PATH = '/Users/sunyunong/Downloads/final.jpg' # 图片转换后的地址
image_names=[]

for i in range(25):#顺序排列list中的元素
    image_names.append(str(i)+'.jpg')

# 获取图片集地址下的所有图片名称
#image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
#        os.path.splitext(name)[1] == item]
#print(image_names)  
# 简单的对于参数的设定和实际图片集的大小进行数量判断
if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
  raise ValueError("合成图片的参数和要求的数量不能匹配！")
  
# 定义图像拼接函数
def image_compose():
  to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE)) #创建一个新图
  # 循环遍历，把每张图片按顺序粘贴到对应位置上
  for y in range(1, IMAGE_ROW + 1):
    for x in range(1, IMAGE_COLUMN + 1):
      from_image = Image.open(IMAGES_PATH + image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
        (IMAGE_SIZE, IMAGE_SIZE),Image.ANTIALIAS)
      to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
  return to_image.save(IMAGE_SAVE_PATH) # 保存新图
image_compose() #调用函数