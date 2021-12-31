import numpy as np
import cv2

# use the webcam to capture live video feed
cap = cv2.VideoCapture(0)

# read the background previously prepared
background = cv2.imread("./bck.jpg")

while cap.isOpened():
    # get the current frame
    # default BGR format
    ret, curr_frame = cap.read()

    if not ret:
        continue

    # convert into HSV format
    # easier color detection when wrinkles / shadows present
    curr_hsv = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2HSV)

    # mask for a 'color'-colored cloak
    CLOAK_COLOR = np.uint8([[[0, 110, 0]]])
    CLOAK_HSV = cv2.cvtColor(CLOAK_COLOR, cv2.COLOR_BGR2HSV)

    CLOAK_LOWER = np.array([CLOAK_HSV[0][0][0] - 20, 50, 50])
    CLOAK_UPPER = np.array([CLOAK_HSV[0][0][0] + 20, 255, 255])
    
    mask = cv2.inRange(curr_hsv, CLOAK_LOWER, CLOAK_UPPER)

    # removing noise
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,
            # np.ones((3, 3), np.uint8), iterations = 10)

    # dilating the edges to smoothen and fatten them
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE,
            np.ones((3, 3), np.uint8), iterations = 1)

    # testing the mask
    # cv2.imshow("mask", mask)
    # if cv2.waitKey(5) == ord('q'):
    #    break

    # the masked regions substituted with background
    masked = cv2.bitwise_and(background, background,
            mask = mask)

    # the unmasked regions shown visible
    unmasked = cv2.bitwise_and(curr_frame, curr_frame,
            mask = cv2.bitwise_not(mask))

    # combining masked and visible regions
    cv2.imshow("magic", masked + unmasked)
    
    # press 'q' to exit
    if (cv2.waitKey(5) == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
