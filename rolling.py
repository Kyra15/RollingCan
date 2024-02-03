# import packages
import cv2
import numpy as np


# apply all the preliminary filters (grayscale, gaussian blue, and canny edge)
def testdect(pic):
    gauss_pic = cv2.GaussianBlur(pic, (15, 15), 0)
    bw_gauss_pic = cv2.cvtColor(gauss_pic, cv2.COLOR_BGR2GRAY)
    canny_gauss_bw_pic = cv2.Canny(bw_gauss_pic, 50, 70)
    return pic, canny_gauss_bw_pic


# detect and output the cricles detected using open cv's HoughCircles
def detection(og, pic):
    # detect the circles with the HoughCircles function
    detected_circles = cv2.HoughCircles(pic, cv2.HOUGH_GRADIENT, 1, 20,
                                        param1=50, param2=10, minRadius=275,
                                        maxRadius=300)

    # make sure at least some circles were detected
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        # get the first parameters from the circle that is detected
        first_circle = detected_circles[0][0]

        # get the parameters for the center coordinates
        # and the radius of the first circle detected
        x, y, r = first_circle[0], first_circle[1], first_circle[2]

        # draw the circle for the circumference of the can
        cv2.circle(og, (x, y), r, (70, 255, 133), 16)

        # draw the smaller circle for the center of the circle
        cv2.circle(og, (x, y), 1, (70, 255, 133), 18)

        return og
    else:
        # if no circles are detected print "no circle" in the console and return the original image
        print("no circle")
        return og


# function for saving the final overlayed video
def writeVideo():
    # get the screen resolution of the frame
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    size = (frame_width, frame_height)

    # use theVideoWriter function to create a new video file
    # with the previously obtained screen resolution
    final = cv2.VideoWriter('writtenvid.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
    return final


# create video capture object
video = cv2.VideoCapture("rollingcan4.mov")

# this line calls the function for saving the file
final = writeVideo()

while video.isOpened():
    # read each frame
    ret, frame = video.read()
    if ret:
        # call the function that applies filters on the frame
        frame, test = testdect(frame)

        # this line creates the actual file for the new video
        final.write(detection(frame, test))

        # detect and draw the Hough Circles by calling the detection function
        detected_frame = detection(frame, test)

        # show the frame
        cv2.imshow("Detected Frame", detected_frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# stop the 2 video capture objects and destroy all of the open cv windows
video.release()
final.release()
cv2.destroyAllWindows()
