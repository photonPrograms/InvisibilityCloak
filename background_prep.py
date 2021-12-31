import numpy as np
import cv2

# capturing the video from webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # getting the background from the current frame
    ret, background = cap.read()
    
    # if read successfully, display the background
    if ret:
        cv2.imshow("background", background)
        
        # if 'q' for quit pressed, save the background
        if cv2.waitKey(5) == ord('q'):
            cv2.imwrite("bck.jpg", background)
            break

cap.release()
cv2.destroyAllWindows()
