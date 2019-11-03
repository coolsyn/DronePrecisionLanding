'''

    Synopsis: Script to simulate the drone's vision.
    Author: Daniel Nugent
    Code Available at https://github.com/djnugent/Precland/blob/master/PrecisionLand_lib/PL_sim.py used under the GNU license

'''

#Opencv Imports
import cv2
import numpy as np

#Python Imports
import math
import time
import os

#Dronekit Imports
from dronekit import VehicleMode, Attitude, connect, LocationGlobalRelative
from dronekit_sitl import SITL

#Common Library Imports
from position_vector import PositionVector
import flight_assist as flightAssist

#List of global variables
targetLocation = PositionVector()
vehicleLocation = PositionVector()
vehicleAttitude = 0
backgroundColor = (74,88,109)
filename = (os.path.dirname(os.path.realpath(__file__)))+"/Resources/target.PNG"
target_size = 1.5
camera_width = 640
camera_height = 480
camera_vfov = 60
camera_hfov = 60
camera_fov = math.sqrt(camera_vfov**2 + camera_hfov**2)
camera_frameRate = 30
current_milli_time = lambda: int(round(time.time() * 1000))

def load_target(filename, actualS=1.5):
	global target, target_width, target_height
	global actualSize
	target = cv2.imread(filename)
	target_width = target.shape[1]
	target_height = target.shape[0]
	actualSize = actualS
	global pixels_per_meter
	pixels_per_meter = (target_height + target_width) / (2.0 * actualSize)

def set_target_location(location):
	targetLocation.set_from_location(location)

def project_3D_to_2D(thetaX,thetaY,thetaZ, aX, aY,aZ, cX, cY, cZ, height, width, fov):
	dX = math.cos(-thetaY) * (math.sin(-thetaZ)*(cY-aY) + math.cos(-thetaZ)*(cX-aX)) - math.sin(-thetaY)*(aZ-cZ)
	dY = math.sin(-thetaX) * (math.cos(-thetaY)*(aZ-cZ) + math.sin(-thetaY)*(math.sin(-thetaZ)*(cY-aY) + math.cos(-thetaZ)*(cX-aX))) + math.cos(-thetaX)*(math.cos(-thetaZ)*(cY-aY) - math.sin(-thetaZ) * (cX-aX))
	dZ = math.cos(-thetaX) * (math.cos(-thetaY)*(aZ-cZ) + math.sin(-thetaY)*(math.sin(-thetaZ)*(cY-aY) + math.cos(-thetaZ)*(cX-aX))) - math.sin(-thetaX)*(math.cos(-thetaZ)*(cY-aY) - math.sin(-thetaZ) * (cX-aX))

	eX = 0
	eY = 0
	eZ = 1.0/math.tan(math.radians(fov)/2.0)

	bX = (dX - eX)*(eZ/dZ)
	bY = (dY - eY)*(eZ/dZ)

	sX = bX * width
	sY = bY * height

	return (sX,sY)

def shift_to_image(pt,width,height):
	return ((pt[0] + width/2),(-1*pt[1] + height/2.0))

def simulate_target(thetaX,thetaY,thetaZ, aX, aY, aZ, cX, cY, cZ, camera_height, camera_width, fov):
	img_width = target_width
	img_height = target_height
	corners = np.float32([[-img_width/2,img_height/2],[img_width/2 ,img_height/2],[-img_width/2,-img_height/2],[img_width/2, -img_height/2]])
	newCorners = np.float32([[0,0],[0,0],[0,0],[0,0]])
	for i in range(0,len(corners)):
		x = corners[i][0] + cX - img_width/2.0
		y = corners[i][1] + cY - img_height/2.0
		x , y = project_3D_to_2D(thetaX,thetaY,thetaZ, aY, aX, aZ, y, x, cZ,camera_height,camera_width,fov)
		x , y = shift_to_image((x,y),camera_width,camera_height)
		newCorners[i] = x,y  

	M = cv2.getPerspectiveTransform(corners,newCorners)

	#im = cv2.imread("Resources/bg.jpg")
	#im = cv2.resize(im, (640,480))
	sim = cv2.warpPerspective(target,M,(640, 480),borderValue=(74,88,109))

	return sim

def get_frame(vehicleAttitude):
	start = current_milli_time()
	aX,aY,aZ = targetLocation.x, targetLocation.y, targetLocation.z
	cX,cY,cZ = vehicleLocation.x, vehicleLocation.y, vehicleLocation.z

	thetaX = vehicleAttitude.pitch
	thetaY = vehicleAttitude.roll
	thetaZ = vehicleAttitude.yaw
	aX = aX * pixels_per_meter
	aY = aY * pixels_per_meter
	aZ = aZ * pixels_per_meter
	cX = cX * pixels_per_meter
	cY = cY * pixels_per_meter
	cZ = cZ * pixels_per_meter

	sim = simulate_target(thetaX,thetaY,thetaZ, aX, aY, aZ, cX, cY, cZ, camera_height, camera_width, camera_fov)
	
	while(1000/camera_frameRate > current_milli_time() - start):
		pass
	return sim

def refresh_simulator(vehicleLoc, vehicleAtt):
	vehicleLocation.set_from_location(vehicleLoc)
	vehicleAttitude = vehicleAtt

if __name__ == '__main__':
	load_target(filename, target_size)
	sitl = SITL()
	sitl.download('copter', '3.3', verbose=True)
	sitl_args = ['-I0', '--model', 'quad', '--home=-35.363261,149.165230,584,353']
	sitl.launch(sitl_args, await_ready=True, restart=True)
	connection_string = "tcp:127.0.0.1:5760"
	print("Connecting to vehicle on: %s" % connection_string)
	veh_control = connect(connection_string, wait_ready=True)

	set_target_location(veh_control.location.global_relative_frame)

	flightAssist.arm_and_takeoff(veh_control, 15)

	while (veh_control is not None):
		location = veh_control.location.global_relative_frame
		attitude = veh_control.attitude

		refresh_simulator(location,attitude)
		frame = get_frame(attitude)
		cv2.imshow('frame',frame)
		key = cv2.waitKey(1)
		print(key)

		if key == ord('w'):
			flightAssist.send_ned_velocity(veh_control, 2, 0, 0, 1) #forward
		elif key == ord('s'):
			flightAssist.send_ned_velocity(veh_control, -2, 0, 0, 1) #backward
		elif key == ord('a'):
			flightAssist.send_ned_velocity(veh_control, 0, -2, 0, 1) #left
		elif key == ord('d'):
			flightAssist.send_ned_velocity(veh_control, 0, 2, 0, 1) #right
		elif(key == ord('q')):
			yaw = math.degrees(attitude.yaw) #yaw left
			flightAssist.condition_yaw(veh_control, yaw-5)
		elif(key == ord('e')):
			yaw = math.degrees(attitude.yaw) #yaw right
			flightAssist.condition_yaw(veh_control,yaw + 5)
		elif(key == ord('8')):
			flightAssist.send_ned_velocity(veh_control, 0, 0, -2, 1) #down
		elif(key == ord('2')):
			flightAssist.send_ned_velocity(veh_control, 0,0,2, 1) #up
		elif (key == ord('1')):
			break
		else:
			flightAssist.send_ned_velocity(veh_control,0,0,0,1) #still
	
	print("Returning to Launch")
	veh_control.mode = VehicleMode("RTL")
	print("Close vehicle object")
	veh_control.close()
	if sitl is not None:
	    sitl.stop()
