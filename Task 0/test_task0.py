
'''
*****************************************************************************************
*
*        =================================================
*             Berryminator (BM) Theme (eYRC 2021-22)
*        =================================================
*
*  This script is intended to check the versions of the installed
*  software/libraries in Task 0 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  Filename:			test_task0.py
*  Created:				25/09/2021
*  Last Modified:		25/09/2021
*  Author:				e-Yantra Team
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*
*****************************************************************************************
'''


# Import test module
try:
	import task0_cardinal

except ImportError:
	print("\n\t[ERROR] It seems that task0_cardinal.pyc is not found in current directory! OR")
	print("\n\tAlso, it might be that you are running test_task0.py from outside the Conda environment!\n")
	exit()


# Main function
if __name__ == '__main__':

	task0_cardinal.test_setup()

