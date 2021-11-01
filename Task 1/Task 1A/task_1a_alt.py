'''
*****************************************************************************************
*
*        		===============================================
*           		Berryminator (BM) Theme (eYRC 2021-22)
*        		===============================================
*
*  This script is to implement Task 1A of Berryminator(BM) Theme (eYRC 2021-22).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			1387
# Author List:		Aaditya Pramod, Ayush Gupta, Muntaba Khan, Pranjal
# Filename:			task_1a.py
# Functions:		detect_shapes
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, os)                ##
##############################################################
import cv2
import numpy as np
import os
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################


##############################################################

def detect_shapes(img):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a nested list
    containing details of colored (non-white) shapes in that image

    Input Arguments:
    ---
    `img` :	[ numpy array ]
                    numpy array of image returned by cv2 library

    Returns:
    ---
    `detected_shapes` : [ list ]
                    nested list containing details of colored (non-white)
                    shapes present in image

    Example call:
    ---
    shapes = detect_shapes(img)
    """
    detected_shapes = []


    ##############	ADD YOUR CODE HERE	##############
    name,coords,col="",(0,0),""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours[1:]:
        approx=cv2.approxPolyDP(contour,0.025*cv2.arcLength(contour,True),True)
        M=cv2.moments(contour)
        if M['m00']!=0.0:
            x=int(M['m10']/M['m00'])            #coords of centroid
            y=int(M['m01']/M['m00'])
            coords=(x,y)

        if len(approx)==3:
            name="Triangle"

        if len(approx)==4:
            ((a,b),(w,h),(r))=cv2.minAreaRect(approx)
            if (float(w)/h)==1:
                name="Square"
            else:
                name="Rectangle"
        if len(approx)==5:
            name="Pentagon"
        if len(approx)>7:
            name="Circle"

        (b,g,r)=img[y,x]
        if (b,g,r)==(255,0,0):
            col="Blue"
        if (b,g,r)==(0,255,0):
            col="Green"
        if (b,g,r)==(0,0,255):
            col="Red"
        if (b,g,r)==(0,140,255) or (b,g,r)==(0,150,255):
            col="Orange"
        detected_shapes+=[[col,name,coords]]


    ##################################################

    return detected_shapes


def get_labeled_image(img, detected_shapes):
    ######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########
    """
    Purpose:
    ---
    This function takes the image and the detected shapes list as an argument
    and returns a labelled image

    Input Arguments:
    ---
    `img` :	[ numpy array ]
                    numpy array of image returned by cv2 library

    `detected_shapes` : [ list ]
                    nested list containing details of colored (non-white)
                    shapes present in image

    Returns:
    ---
    `img` :	[ numpy array ]
                    labelled image

    Example call:
    ---
    img = get_labeled_image(img, detected_shapes)
    """
    ######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########

    for detected in detected_shapes:
        colour = detected[0]
        shape = detected[1]
        coordinates = detected[2]
        cv2.putText(img, str((colour, shape)), coordinates,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    return img


if __name__ == '__main__':

    # path directory of images in 'test_images' folder
    img_dir_path = 'test_images/'

    # path to 'test_image_1.png' image file
    file_num = 1
    img_file_path = img_dir_path + 'test_image_' + str(file_num) + '.png'

    # read image using opencv
    img = cv2.imread(img_file_path)

    print('\n============================================')
    print('\nFor test_image_' + str(file_num) + '.png')

    # detect shape properties from image
    detected_shapes = detect_shapes(img)
    print(detected_shapes)

    # display image with labeled shapes
    img = get_labeled_image(img, detected_shapes)
    cv2.imshow("labeled_image", img)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

    choice = input(
        '\nDo you want to run your script on all test images ? => "y" or "n": ')

    if choice == 'y':

        for file_num in range(1, 16):

            # path to test image file
            img_file_path = img_dir_path + \
                'test_image_' + str(file_num) + '.png'

            # read image using opencv
            img = cv2.imread(img_file_path)

            print('\n============================================')
            print('\nFor test_image_' + str(file_num) + '.png')

            # detect shape properties from image
            detected_shapes = detect_shapes(img)
            print(detected_shapes)

            # display image with labeled shapes
            img = get_labeled_image(img, detected_shapes)
            cv2.imshow("labeled_image", img)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
