'''
*****************************************************************************************
*
*        		===============================================
*           		Berryminator (BM) Theme (eYRC 2021-22)
*        		===============================================
*
*  This script is to implement Task 4 of Berryminator(BM) Theme (eYRC 2021-22).
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
# Filename:			task_4.py
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

import task_1a
import task_1b
import task_2a
import task_3

################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

##############################################################


def detect_berries(client_id):
    return_code, vision_sensor1_handle = sim.simxGetObjectHandle(
        client_id, 'vision_sensor_1', sim.simx_opmode_blocking)
    vision_sensor1_image, res, return_code = task_2a.get_vision_sensor_image(
        client_id, vision_sensor1_handle)
    vision_sensor1_depth, dres, dreturn_code = task_2a.get_vision_sensor_depth_image(
        client_id, vision_sensor1_handle)
    trans_vis_img = task_1b.transform_vision_sensor_image(
        vision_sensor1_image, res)
    trans_dep_img = task_2a.transformed_depth_image(vision_sensor1_depth, dres)
    berries_dict = task_2a.detect_berries(trans_vis_img, trans_dep_img)
    berries_pos_dict = task_2a.detect_berry_positions(berries_dict)
    return berries_pos_dict


def curr_pos(client_id):
    return_code, vision_sensor2_handle = sim.simxGetObjectHandle(
        client_id, 'vision_sensor_2', sim.simx_opmode_blocking)
    vision_sensor2_image, res, return_code = task_2a.get_vision_sensor_image(
        client_id, vision_sensor2_handle)
    coords = task_3.detect_qr_codes(vision_sensor2_image, client_id)
    return coords


def navigation(coords):
    #set of points to traverse through without passing through obstacles
    targets = [2,4]
    pass


def pick(client_id, berries_pos):
    #pick up the berry
    pass


def drop(client_id):
    #drop into the basket
    pass



def send_identified_berry_data(client_id, berry_name, x_coor, y_coor, depth):
    """
	Purpose:
	---
	Teams should call this function as soon as they identify a berry to pluck. This function should be called only when running via executable.
	
	NOTE: 
	1. 	Correct Pluck marks will only be awarded if the team plucks the last detected berry. 
		Hence before plucking, the correct berry should be identified and sent via this function.

	2.	Accuracy of detection should be +-0.025m.

	Input Arguments:
	---
	`client_id` 	:  [ integer ]
		the client_id generated from start connection remote API, it should be stored in a global variable

	'berry_name'		:	[ string ]
			name of the detected berry.

	'x_coor'			:	[ float ]
			x-coordinate of the centroid of the detected berry.

	'y_coor'			:	[ float ]
			y-coordinate of the centroid of the detected berry.

	'depth'			:	[ float ]
			z-coordinate of the centroid of the detected berry.

	Returns:
	---
	`return_code`		:	[ integer ]
			A remote API function return code
			https://www.coppeliarobotics.com/helpFiles/en/remoteApiConstants.htm#functionErrorCodes

	Example call:
	---
	return_code=send_identified_berry_data(berry_name,x_coor,y_coor)
	
	"""
    ##################################################
    ## You are NOT allowed to make any changes in the code below. ##
    emptybuff = bytearray()

    if (type(berry_name) != str):
        berry_name = str(berry_name)

    if (type(x_coor) != float):
        x_coor = float(x_coor)

    if (type(y_coor) != float):
        y_coor = float(y_coor)

    if (type(depth) != float):
        depth = float(depth)

    data_to_send = [berry_name, str(x_coor), str(y_coor), str(depth)]
    return_code, outints, oufloats, outstring, outbuffer = sim.simxCallScriptFunction(
        client_id, 'eval_bm', sim.sim_scripttype_childscript,
        'detected_berry_by_team', [], [], data_to_send, emptybuff,
        sim.simx_opmode_blocking)
    return return_code

    ##################################################


def getDistance(positions):
    return positions[2]


def task_4_primary(client_id):
    """
	Purpose:
	---
	This is the only function that is called from the main function. Make sure to fill it
	properly, such that the bot traverses to the vertical rack, detects, plucks & deposits a berry of each color.

	Input Arguments:
	---
	`client_id`         :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()

	
	Returns:
	---
	
	Example call:
	---
	task_4_primary(client_id)
	"""
    lberry = ["Strawberry", "Blueberry", "Lemon"]
    task_3.task_3_primary(client_id, [(0, 6), (4, 6)])
    for i in range(3):
        berries_pos = detect_berries(client_id)
        berries_pos = berries_pos[lberry[i]]
        if berries_pos == []:
            if lberry[i] == "Strawberry":
                task_3.task_3_primary(client_id, [(4, 7)])
            else:
                task_3.task_3_primary(client_id, [(4, 5)])

        while berries_pos == []:
            berries_pos = detect_berries(client_id)
            berries_pos = berries_pos[lberry[i]]

        berries_pos.sort(key=getDistance)
        berry = berries_pos[0]
        send_identified_berry_data(client_id, lberry[i], berry[0], berry[1],
                                   berry[2])
        coords = curr_pos(client_id)
        #targets = navigation(coords)
        #task_3.task_3_primary(client_id, targets)
        pick(client_id, berries_pos)
        #targets = navigation()
        task_3.task_3_primary(client_id, [(2,4)])
        drop(client_id)
        task_3.task_3_primary(client_id, [(0, 6), (4, 6)])


if __name__ == "__main__":

    ##################################################
    ## You are NOT allowed to make any changes in the code below ##

    # Initiate the Remote API connection with CoppeliaSim server
    print('\nConnection to CoppeliaSim Remote API Server initiated.')
    print('Trying to connect to Remote API Server...')

    try:
        client_id = task_1b.init_remote_api_server()
        if (client_id != -1):
            print(
                '\nConnected successfully to Remote API Server in CoppeliaSim!'
            )

            # Starting the Simulation
            try:
                return_code = task_1b.start_simulation()

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

        task_4_primary(client_id)
        time.sleep(1)

        try:
            return_code = task_1b.stop_simulation(client_id)
            if (return_code == sim.simx_return_ok) or (
                    return_code == sim.simx_return_novalue_flag):
                print('\nSimulation stopped correctly.')

                # Stop the Remote API connection with CoppeliaSim server
                try:
                    task_1b.exit_remote_api_server(client_id)
                    if (task_1b.start_simulation(client_id) ==
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
            '\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!'
        )
        print('Stop the CoppeliaSim simulation manually if started.\n')
        traceback.print_exc(file=sys.stdout)
        print()
        sys.exit()
