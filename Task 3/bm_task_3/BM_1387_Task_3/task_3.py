'''
*****************************************************************************************
*
*        		===============================================
*           		Berryminator (BM) Theme (eYRC 2021-22)
*        		===============================================
*
*  This script is to implement Task 3 of Berryminator(BM) Theme (eYRC 2021-22).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_3.py
# Functions:
# Global variables:
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the given available ##
## modules for this task                                    ##
##############################################################

import cv2
import numpy as np
import os, sys
import traceback
import math
import time
import sys
from pyzbar.pyzbar import decode

##############################################################

# Importing the sim module for Remote API connection with CoppeliaSim
try:
    import sim

except Exception:
    print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
    print('\n[WARNING] Make sure to have following files in the directory:')
    print(
        'sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n'
    )
    sys.exit()

################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

##############################################################


def init_remote_api_server():
	"""
	Purpose:
	---
	This function should first close any open connections and then start
	communication thread with server i.e. CoppeliaSim.
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	`client_id` 	:  [ integer ]
		the client_id generated from start connection remote API, it should be stored in a global variable
	
	Example call:
	---
	client_id = init_remote_api_server()
	
	"""
	global client_id
	client_id = -1

    ##############	ADD YOUR CODE HERE	##############
	sim.simxFinish(-1)
	client_id = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

    ##################################################
	return client_id


def start_simulation(client_id):
    """
	Purpose:
	---
	This function should first start the simulation if the connection to server
	i.e. CoppeliaSim was successful and then wait for last command sent to arrive
	at CoppeliaSim server end.
	
	Input Arguments:
	---
	`client_id`    :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()

	Returns:
	---
	`return_code` 	:  [ integer ]
		the return code generated from the start running simulation remote API
	
	Example call:
	---
	return_code = start_simulation()
	
	"""
    return_code = -2

    ##############	ADD YOUR CODE HERE	##############
    return_code = sim.simxStartSimulation(client_id, sim.simx_opmode_oneshot)

    ##################################################

    return return_code


def get_vision_sensor_image(client_id):
    """
	Purpose:
	---
	This function should first get the handle of the Vision Sensor object from the scene.
	After that it should get the Vision Sensor's image array from the CoppeliaSim scene.
	Input Arguments:
	---
	`client_id`    :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()
	
	Returns:
	---
	`vision_sensor_image` 	:  [ list ]
		the image array returned from the get vision sensor image remote API
	`image_resolution` 		:  [ list ]
		the image resolution returned from the get vision sensor image remote API
	`return_code` 			:  [ integer ]
		the return code generated from the remote API
	
	Example call:
	---
	vision_sensor_image, image_resolution, return_code = get_vision_sensor_image()
	"""

    return_code = 0

    ##############	ADD YOUR CODE HERE	##############
    res, v0 = sim.simxGetObjectHandle(client_id, 'vision_sensor_1',
                                      sim.simx_opmode_oneshot_wait)
    return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(
        client_id, v0, 0, sim.simx_opmode_oneshot_wait)

    ##################################################

    return vision_sensor_image, image_resolution, return_code


def transform_vision_sensor_image(vision_sensor_image, image_resolution):
	"""
	Purpose:
	---
	This function should:
	1. First convert the vision_sensor_image list to a NumPy array with data-type as uint8.
	2. Since the image returned from Vision Sensor is in the form of a 1-D (one dimensional) array,
	the new NumPy array should then be resized to a 3-D (three dimensional) NumPy array.
	3. Change the color of the new image array from BGR to RGB.
	4. Flip the resultant image array about the X-axis.
	The resultant image NumPy array should be returned.
	
	Input Arguments:
	---
	`vision_sensor_image` 	:  [ list ]
		the image array returned from the get vision sensor image remote API
	`image_resolution` 		:  [ list ]
		the image resolution returned from the get vision sensor image remote API
	
	Returns:
	---
	`transformed_image` 	:  [ numpy array ]
		the resultant transformed image array after performing above 4 steps
	
	Example call:
	---
	transformed_image = transform_vision_sensor_image(vision_sensor_image, image_resolution)
	
	"""
	transformed_image = None

    ##############	ADD YOUR CODE HERE	##############
	image = np.array(np.uint8(vision_sensor_image))
    #print(image.reshape((image_resolution[1],-1)).shape)
    #print(min(image))
	transformed_image = np.reshape(
        image, [image_resolution[0], image_resolution[1], 3])
	transformed_image = cv2.flip(transformed_image, 0)
	transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2GRAY)

    ##################################################
	return transformed_image


def stop_simulation(client_id):
    """
	Purpose:
	---
	This function should stop the running simulation in CoppeliaSim server.
	NOTE: In this Task, do not call the exit_remote_api_server function in case of failed connection to the server.
		  It is already written in the main function.
	
	Input Arguments:
	---
	`client_id`    :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()
	
	Returns:
	---
	`return_code` 	:  [ integer ]
		the return code generated from the stop running simulation remote API
	
	Example call:
	---
	return_code = stop_simulation()
	
	"""

    return_code = -2

    ##############	ADD YOUR CODE HERE	##############
    return_code = sim.simxStopSimulation(client_id, sim.simx_opmode_oneshot)

    ##################################################

    return return_code


def exit_remote_api_server(client_id):
    """
	Purpose:
	---
	This function should wait for the last command sent to arrive at the Coppeliasim server
	before closing the connection and then end the communication thread with server
	i.e. CoppeliaSim using simxFinish Remote API.
	Input Arguments:
	---
	`client_id`    :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()
	
	Returns:
	---
	None
	
	Example call:
	---
	exit_remote_api_server()
	
	"""

    ##############	ADD YOUR CODE HERE	##############
    sim.simxFinish(client_id)

    ##################################################


def detect_qr_codes(transformed_image,client_id):
	"""
	Purpose:
	---
	This function receives the transformed image from the vision sensor and detects qr codes in the image

	Input Arguments:
	---
	`transformed_image` 	:  [ numpy array ]
		the transformed image array
	
	Returns:
	---
	None
	
	Example call:
	---
	detect_qr_codes()
	
	"""

    ##############	ADD YOUR CODE HERE	##############
	global wheel_joints
	point = []
	barcodes = decode(transformed_image)
	for bar in barcodes:
		(x, y, w, h) = bar.rect
		data = bar.data.decode("utf-8")
		data=data[1:-1].split(",")
		point=[int(i) for i in data]
		if x<10:
			set_bot_movement(client_id,wheel_joints,0,-2,0)
		elif x+w>110:
			set_bot_movement(client_id,wheel_joints,0,2,0)
		elif y<10:
			set_bot_movement(client_id,wheel_joints,1,0,0)
		elif y+h>110:
			set_bot_movement(client_id,wheel_joints,-1,0,0)

		

		
		#qr_codes.append(data)

    ##################################################
	return point


def set_bot_movement(client_id, wheel_joints, forw_back_vel, left_right_vel,
                     rot_vel):
	"""
	Purpose:
	---
	This function takes desired forward/back, left/right, rotational velocites of the bot as input arguments.
	It should then convert these desired velocities into individual joint velocities(4 joints) and actuate the joints
	accordingly.

	Input Arguments:
	---
	`client_id`         :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()

	'wheel_joints`      :   [ list]
		Python list containing joint object handles of individual joints

	`forw_back_vel'     :   [ float ]
		Desired forward/back velocity of the bot

	`left_right_vel'    :   [ float ]
		Desired left/back velocity of the bot
	
	`rot_vel'           :   [ float ]
		Desired rotational velocity of the bot
	
	Returns:
	---
	None
	
	Example call:
	---
	set_bot_movement(client_id, wheel_joints, 0.5, 0, 0)
	"""

    ##############	ADD YOUR CODE HERE	##############
	vel=[0,0,0,0]
	#FORWARD BACKWARD MOTION
	# sim.simxSetJointTargetVelocity(client_id,wheel_joints[0],forw_back_vel,sim.simx_opmode_oneshot)
	# sim.simxSetJointTargetVelocity(client_id,wheel_joints[1],forw_back_vel,sim.simx_opmode_oneshot)
	# sim.simxSetJointTargetVelocity(client_id,wheel_joints[2],forw_back_vel,sim.simx_opmode_oneshot)
	# sim.simxSetJointTargetVelocity(client_id,wheel_joints[3],forw_back_vel,sim.simx_opmode_oneshot)
	vel[0]+=forw_back_vel
	vel[1]+=forw_back_vel
	vel[2]+=forw_back_vel
	vel[3]+=forw_back_vel

	#LEFT RIGHT MOTION
	# sim.simxSetJointTargetVelocity(client_id,wheel_joints[0],left_right_vel*math.sqrt(2),sim.simx_opmode_oneshot)
	# sim.simxSetJointTargetVelocity(client_id,wheel_joints[1],-left_right_vel*math.sqrt(2),sim.simx_opmode_oneshot)
	# sim.simxSetJointTargetVelocity(client_id,wheel_joints[2],-left_right_vel*math.sqrt(2),sim.simx_opmode_oneshot)
	# sim.simxSetJointTargetVelocity(client_id,wheel_joints[3],left_right_vel*math.sqrt(2),sim.simx_opmode_oneshot)
	vel[0]+=-left_right_vel
	vel[1]+=left_right_vel
	vel[2]+=left_right_vel
	vel[3]+=-left_right_vel

	#ROTATION
	# sim.simxSetJointTargetVelocity(client_id,wheel_joints[0],rot_vel,sim.simx_opmode_oneshot)
	# sim.simxSetJointTargetVelocity(client_id,wheel_joints[1],-rot_vel,sim.simx_opmode_oneshot)
	# sim.simxSetJointTargetVelocity(client_id,wheel_joints[2],rot_vel,sim.simx_opmode_oneshot)
	# sim.simxSetJointTargetVelocity(client_id,wheel_joints[3],-rot_vel,sim.simx_opmode_oneshot)
	vel[0]+=-rot_vel
	vel[1]+=rot_vel
	vel[2]+=-rot_vel
	vel[3]+=rot_vel

	sim.simxSetJointTargetVelocity(client_id,wheel_joints[0],vel[0],sim.simx_opmode_streaming)
	sim.simxSetJointTargetVelocity(client_id,wheel_joints[1],vel[1],sim.simx_opmode_streaming)
	sim.simxSetJointTargetVelocity(client_id,wheel_joints[2],vel[2],sim.simx_opmode_streaming)
	sim.simxSetJointTargetVelocity(client_id,wheel_joints[3],vel[3],sim.simx_opmode_streaming)



    ##################################################


def init_setup(client_id):
	"""
	Purpose:
	---
	This function will get the object handles of all the four joints in the bot, store them in a list
	and return the list

	Input Arguments:
	---
	`client_id`         :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()
	
	Returns:
	---
	'wheel_joints`      :   [ list]
		Python list containing joint object handles of individual joints
	
	Example call:
	---
	init setup(client_id)
	
	"""

    ##############	ADD YOUR CODE HERE	##############
	global wheel_joints
	wheel_joints=[]
	wheels = ['fr', 'fl', 'rr', 'rl']
	wheel_joints = [
        sim.simxGetObjectHandle(client_id, f'rollingJoint_{i}',
                                sim.simx_opmode_oneshot_wait)[1]
        for i in wheels
    ]
    ##################################################
	return wheel_joints


def encoders(client_id):
    """
	Purpose:
	---
	This function will get the `combined_joint_position` string signal from CoppeliaSim, decode it
	and return a list which contains the total joint position of all joints    

	Input Arguments:
	---
	`client_id`         :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()
	
	Returns:
	---
	'joints_position`      :   [ list]
		Python list containing the total joint position of all joints
	
	Example call:
	---
	encoders(client_id)
	
	"""

    return_code, signal_value = sim.simxGetStringSignal(
        client_id, 'combined_joint_position', sim.simx_opmode_blocking)
    signal_value = signal_value.decode()
    joints_position = signal_value.split("%")

    for index, joint_val in enumerate(joints_position):
        joints_position[index] = float(joint_val)

    return joints_position


def nav_logic(curr_coord,next_coord,vel):
	"""
	Purpose:
	---
	This function should implement your navigation logic. 
	"""
	#------------------------------
	# GRID MOVEMENTS
	#------------------------------
	x,y=curr_coord
	X,Y=next_coord
	forw_vel,left_right_vel,rot_vel=0,0,0
	if x<X:
		left_right_vel=vel
	elif x>X:
		left_right_vel=-vel
	elif x==X:
		if y<Y:
			forw_vel=vel
		elif y>Y:
			forw_vel=-vel
	
	return forw_vel,left_right_vel,rot_vel

def shortest_path():
    """
	Purpose:
	---
	This function should be used to find the shortest path on the given floor between the destination and source co-ordinates.
	"""


def task_3_primary(client_id, target_points):
	"""
	Purpose:
	---
	
	# NOTE:This is the only function that is called from the main function and from the executable.

	Make sure to call all the necessary functions (apart from the ones called in the main) according to your logic. 
	The bot should traverses all the target navigational co-ordinates.

	Input Arguments:
	---
	`client_id`         :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()

	`target_points`     : [ list ]
		List of tuples where tuples are the target navigational co-ordinates.
	
	Returns:
	---
	
	Example call:
	---
	target_points(client_id, target_points)
	"""
	# NOTE:max achievable speed without errors is 7
	global x
	x=[0,0]
	wheel_joints=init_setup(client_id)
	img,res,ret=get_vision_sensor_image(client_id)
	img=transform_vision_sensor_image(img,res)
	temp=detect_qr_codes(img,client_id)
	if len(temp)==2:
		x=temp

	#print(x)
	for target_point in target_points:
		while x != list(target_point):
			forw_vel,left_right_vel,rot_vel=nav_logic(x,target_point,7)
			set_bot_movement(client_id,wheel_joints,forw_vel,left_right_vel,rot_vel)
			img,res,ret=get_vision_sensor_image(client_id)
			img=transform_vision_sensor_image(img,res)
			temp=detect_qr_codes(img,client_id)
			if len(temp)==2:
				x=temp

			#print(x,target_point)
	
	set_bot_movement(client_id,wheel_joints,0,0,0)

	
	# i=0
	# while(i!='x'):
	# 	i=input()
	# 	if i == 'left':
	# 		set_bot_movement(client_id,wheel_joints,0,-5,0)
	# 	elif i == 'right':
	# 		set_bot_movement(client_id,wheel_joints,0,5,0)
	# 	elif i == 'forw':
	# 		set_bot_movement(client_id,wheel_joints,5,0,0)
	# 	elif i == 'back':
	# 		set_bot_movement(client_id,wheel_joints,-5,0,0)
	# 	elif i == 'rotr':
	# 		set_bot_movement(client_id,wheel_joints,0,0,5)
	# 	elif i == 'rotl':
	# 		set_bot_movement(client_id,wheel_joints,0,0,-5)
	# 	else: 
	# 		set_bot_movement(client_id,wheel_joints,0,0,0)

	# 	img,res,ret=get_vision_sensor_image(client_id)
	# 	img=transform_vision_sensor_image(img,res)
	# 	x=detect_qr_codes(img)
	# 	print(x)
		


if __name__ == "__main__":

    ##################################################
    # target_points is a list of tuples. These tuples are the target navigational co-ordinates
    # target_points = [(x1,y1),(x2,y2),(x3,y3),(x4,y4)...]
    # example:
    target_points = [(2, 3), (3, 6)
                     ]  # You can give any number of different co-ordinates

    ##################################################
    ## NOTE: You are NOT allowed to make any changes in the code below ##

    # Initiate the Remote API connection with CoppeliaSim server
    print('\nConnection to CoppeliaSim Remote API Server initiated.')
    print('Trying to connect to Remote API Server...')

    try:
        client_id = init_remote_api_server()
        if (client_id != -1):
            print(
                '\nConnected successfully to Remote API Server in CoppeliaSim!'
            )

            # Starting the Simulation
            try:
                return_code = start_simulation(client_id)

                if (return_code == sim.simx_return_novalue_flag) or (
                        return_code == sim.simx_return_ok):
                    print('\nSimulation started correctly in CoppeliaSim.')

                else:
                    print(
                        '\n[ERROR] Failed starting the simulation in CoppeliaSim!'
                    )
                    print(
                        'start_simulation function is not configured correctly, check the code!'
                    )
                    print()
                    sys.exit()

            except Exception:
                print(
                    '\n[ERROR] Your start_simulation function throwed an Exception, kindly debug your code!'
                )
                print('Stop the CoppeliaSim simulation manually.\n')
                traceback.print_exc(file=sys.stdout)
                print()
                sys.exit()

        else:
            print('\n[ERROR] Failed connecting to Remote API server!')
            print(
                '[WARNING] Make sure the CoppeliaSim software is running and')
            print(
                '[WARNING] Make sure the Port number for Remote API Server is set to 19997.'
            )
            print(
                '[ERROR] OR init_remote_api_server function is not configured correctly, check the code!'
            )
            print()
            sys.exit()

    except Exception:
        print(
            '\n[ERROR] Your init_remote_api_server function throwed an Exception, kindly debug your code!'
        )
        print('Stop the CoppeliaSim simulation manually if started.\n')
        traceback.print_exc(file=sys.stdout)
        print()
        sys.exit()

    try:

        task_3_primary(client_id, target_points)
        time.sleep(1)

        try:
            return_code = stop_simulation(client_id)
            if (return_code == sim.simx_return_ok) or (
                    return_code == sim.simx_return_novalue_flag):
                print('\nSimulation stopped correctly.')

                # Stop the Remote API connection with CoppeliaSim server
                try:
                    exit_remote_api_server(client_id)
                    if (start_simulation(client_id) ==
                            sim.simx_return_initialize_error_flag):
                        print(
                            '\nDisconnected successfully from Remote API Server in CoppeliaSim!'
                        )

                    else:
                        print(
                            '\n[ERROR] Failed disconnecting from Remote API server!'
                        )
                        print(
                            '[ERROR] exit_remote_api_server function is not configured correctly, check the code!'
                        )

                except Exception:
                    print(
                        '\n[ERROR] Your exit_remote_api_server function throwed an Exception, kindly debug your code!'
                    )
                    print('Stop the CoppeliaSim simulation manually.\n')
                    traceback.print_exc(file=sys.stdout)
                    print()
                    sys.exit()

            else:
                print(
                    '\n[ERROR] Failed stopping the simulation in CoppeliaSim server!'
                )
                print(
                    '[ERROR] stop_simulation function is not configured correctly, check the code!'
                )
                print('Stop the CoppeliaSim simulation manually.')

            print()
            sys.exit()

        except Exception:
            print(
                '\n[ERROR] Your stop_simulation function throwed an Exception, kindly debug your code!'
            )
            print('Stop the CoppeliaSim simulation manually.\n')
            traceback.print_exc(file=sys.stdout)
            print()
            sys.exit()

    except Exception:
        print(
            '\n[ERROR] Your task_3_primary function throwed an Exception, kindly debug your code!'
        )
        print('Stop the CoppeliaSim simulation manually if started.\n')
        traceback.print_exc(file=sys.stdout)
        print()
        sys.exit()
