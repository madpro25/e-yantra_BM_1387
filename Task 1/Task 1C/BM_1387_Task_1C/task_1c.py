'''
*****************************************************************************************
*
*        		===============================================
*           		Berryminator (BM) Theme (eYRC 2021-22)
*        		===============================================
*
*  This script is to implement Task 1C of Berryminator(BM) Theme (eYRC 2021-22).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*
*****************************************************************************************
'''

# Team ID:			1387
# Author List:		Aaditya Pramod, Ayush Gupta, Muntaba Khan, Pranjal
# Filename:			task_1c.py
# Functions:		read_distance_sensor, control_logic
# 					[ Comma separated list of functions in this file ]
# Global variables:
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import sys
import traceback
import time
import os
import math

try:
    import sim

except Exception:
    print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
    print('\n[WARNING] Make sure to have following files in the directory:')
    print(
        'sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n'
    )
    sys.exit()

try:
    import task_1b

except ImportError:
    print('\n[ERROR] task_1b.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_1b.py is present in this current directory.\n')
    sys.exit()

except Exception as e:
    print('Your task_1b.py throwed an Exception, kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)
    sys.exit()

##############################################################

i = 0


def read_distance_sensor(client_id, sensor_handle):
    """
	Purpose:
	---
	This function returns the distance from a proximity sensor

	Input Arguments:
	---
	`client_id`    :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()

	`sensor_handle`  : [ integer ]
	    handle of the proximity sensor

	Returns:
	---
	`detected`   :  [ boolean ]
	    returns True if proximity sensor detects wall and False if no wall is detected.
	
	`distance`   :  [ float ]
	    returns the closest distance from wall if wall is detected, returns -1 if no wall is detected.

	Example call:
	---
	detected, distance = read_distance_sensor(client_id, sensor_handle)
	"""
    distance = -1
    detected = False

    ##############	ADD YOUR CODE HERE	##############
    res, detected, point, objhandle, norm = sim.simxReadProximitySensor(
        client_id, sensor_handle, sim.simx_opmode_streaming)

    if detected:
        distance = math.sqrt(sum([i * i for i in point]))

    #print(detected, distance)
    ##################################################
    return detected, distance


def control_logic(client_id):
    """
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to actuate the rotary joints of the robot in this function, such that
	it traverses the points in given order

	Input Arguments:
	---
	`client_id`    :   [ integer ]
		the client id of the communication thread returned by init_remote_api_server()

	Returns:
	---
	None

	Example call:
	---
	control_logic(client_id)
	"""

    ##############  ADD YOUR CODE HERE  ##############
    global i
    res, d1 = sim.simxGetObjectHandle(client_id, 'distance_sensor_1',
                                      sim.simx_opmode_streaming)
    res, d2 = sim.simxGetObjectHandle(client_id, 'distance_sensor_2',
                                      sim.simx_opmode_streaming)
    res, jl = sim.simxGetObjectHandle(client_id, 'left_joint',
                                      sim.simx_opmode_oneshot)
    res, jr = sim.simxGetObjectHandle(client_id, 'right_joint',
                                      sim.simx_opmode_oneshot)
    det1, dis1 = read_distance_sensor(client_id, d1)
    det2, dis2 = read_distance_sensor(client_id, d2)
    while (not (det1 and dis1 < 0.124)):
        res, d1 = sim.simxGetObjectHandle(client_id, 'distance_sensor_1',
                                          sim.simx_opmode_streaming)
        res, d2 = sim.simxGetObjectHandle(client_id, 'distance_sensor_2',
                                          sim.simx_opmode_streaming)
        det1, dis1 = read_distance_sensor(client_id, d1)
        #print(dis1,"d1")
        det2, dis2 = read_distance_sensor(client_id, d2)
        #print(dis2,"d2")
        if dis2 < 0.127 and dis2 > 0.124:
            sim.simxSetJointTargetVelocity(client_id, jl, 1,
                                           sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(client_id, jr, 1,
                                           sim.simx_opmode_oneshot)
            #print("straight")
        if dis2 > 0.127:
            sim.simxSetJointTargetVelocity(client_id, jl, 1,
                                           sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(client_id, jr, -1,
                                           sim.simx_opmode_oneshot)
            #print("out")

        if dis2 < 0.124:
            sim.simxSetJointTargetVelocity(client_id, jl, -1,
                                           sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(client_id, jr, 1,
                                           sim.simx_opmode_oneshot)
            #print("in")
        sim.simxSetJointTargetVelocity(client_id, jl, 1, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(client_id, jr, 1, sim.simx_opmode_oneshot)


    sim.simxSetJointTargetVelocity(client_id, jl, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(client_id, jr, 0, sim.simx_opmode_oneshot)

    while (1):
        #print("second loop")
        if not (det1):
            break
        res, d1 = sim.simxGetObjectHandle(client_id, 'distance_sensor_1',
                                          sim.simx_opmode_streaming)
        res, d2 = sim.simxGetObjectHandle(client_id, 'distance_sensor_2',
                                          sim.simx_opmode_streaming)
        res, jl = sim.simxGetObjectHandle(client_id, 'left_joint',
                                          sim.simx_opmode_oneshot)
        res, jr = sim.simxGetObjectHandle(client_id, 'right_joint',
                                          sim.simx_opmode_oneshot)
        det1, dis1 = read_distance_sensor(client_id, d1)
        det2, dis2 = read_distance_sensor(client_id, d2)

        sim.simxSetJointTargetVelocity(client_id, jl, -4,
                                       sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(client_id, jr, 4,
                                       sim.simx_opmode_oneshot)

    # while (1):#not (dis2 > 0.12 and dis2 < 0.13)):
    #     print("second loop")
    #     if not (dis2 > 0.12 and dis2 < 0.125):
    #         break
    #     res, d1 = sim.simxGetObjectHandle(client_id, 'distance_sensor_1',
    #                                       sim.simx_opmode_streaming)
    #     res, d2 = sim.simxGetObjectHandle(client_id, 'distance_sensor_2',
    #                                       sim.simx_opmode_streaming)
    #     res, jl = sim.simxGetObjectHandle(client_id, 'left_joint',
    #                                       sim.simx_opmode_oneshot)
    #     res, jr = sim.simxGetObjectHandle(client_id, 'right_joint',
    #                                       sim.simx_opmode_oneshot)
    #     det1, dis1 = read_distance_sensor(client_id, d1)
    #     det2, dis2 = read_distance_sensor(client_id, d2)

    #     sim.simxSetJointTargetVelocity(client_id, jl, -1,
    #                                    sim.simx_opmode_oneshot)
    #     sim.simxSetJointTargetVelocity(client_id, jr, 1,
    #                                    sim.simx_opmode_oneshot)

    #sim.simxSetJointTargetVelocity(client_id, jl, 1, sim.simx_opmode_oneshot)
    #sim.simxSetJointTargetVelocity(client_id, jr, 1, sim.simx_opmode_oneshot)
    #print(i)
    #if i<20:
    while (dis2 > 0.13 or dis2 < 0.12):
        det2, dis2 = read_distance_sensor(client_id, d2)
        if dis2 > 0.13:
            sim.simxSetJointTargetVelocity(client_id, jl, 1,
                                           sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(client_id, jr, -1,
                                           sim.simx_opmode_oneshot)

        if dis2 < 0.12:
            sim.simxSetJointTargetVelocity(client_id, jl, -1,
                                           sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(client_id, jr, 1,
                                           sim.simx_opmode_oneshot)

    sim.simxSetJointTargetVelocity(client_id, jl, 1, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(client_id, jr, 1, sim.simx_opmode_oneshot)
    i+=1
    if i<5:
        control_logic(client_id)

    ##################################################

    ## You are NOT allowed to make any changes in the code below ##


if __name__ == "__main__":

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
                return_code = task_1b.start_simulation(client_id)

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
        control_logic(client_id)
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
