import cv2
import numpy as np
import matplotlib.pyplot as plt

# image = cv2.imread('image.png')
# g = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# edge = cv2.Canny(g, 100, 200)

def gstreamer_pipeline(
    capture_width=3264,
    capture_height=2464,
    display_width=1080,
    display_height=720,
    framerate=21,
    flip_method=2,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def show_camera():
# To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=2))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # # Window
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            ret_val, image = cap.read()
            g = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edge = cv2.Canny(g, 250, 255)
            contours, hierarchy = cv2.findContours(image=edge, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            #cv2.drawContours(image=edge, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                # cv2.circle(image_copy, (cX, cY), 5, (255, 255, 255), -1)
        #     
        #     contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            for c in contours:
                # calculate moments for each contour
                # M = cv2.moments(c)
                # if M["m00"] != 0:
                #     cX = int(M["m10"] / M["m00"])
                #     cY = int(M["m01"] / M["m00"])
                #     print("Centroid: %d, %d" % (cX, cY))
                # else:
                #     cX, cY = 0, 0
                #image_copy = img.copy()
                cv2.drawContours(image=image, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                # cv2.circle(image_copy, (cX, cY), 5, (255, 255, 255), -1)
        #         cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.imshow('CSI Camera', image)
        #     #print("before imshow")
        #     #cv2.waitKey(3000)
        #     #print("after imshow")
        #     #cv2.imwrite('image_thres1.jpg', thresh)
            keyCode = cv2.waitKey(30) & 0xFF
        #Stop the program on the ESC key
            if keyCode == 27:
                cv2.imwrite('image_thres1.jpg', image)
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()