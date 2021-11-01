import cv2 as cv
import numpy as np

img=cv.imread("test_images/test_image_14.png")
cv.imshow("test",img)
cv.waitKey(0)
cv.destroyAllWindows()
