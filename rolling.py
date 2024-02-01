# import packages
import cv2
import numpy as np

def testdect(pic):
    # mask = np.zeros(pic.shape[:2], dtype="uint8")
    # cv2.circle(mask, (500, 400), 500, 255, -1)
    # masked = cv2.bitwise_and(pic, pic, mask=mask)
    bw_pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    gauss_bw_pic = cv2.GaussianBlur(bw_pic, (15, 15), 0)
    canny_gauss_bw_pic = cv2.Canny(gauss_bw_pic, 50, 70)
    return canny_gauss_bw_pic


def detection(pic):
    # convert to grayscale and gaussian blur
    # mask = np.zeros(pic.shape[:2], dtype="uint8")
    # cv2.circle(mask, (500, 500), 400, 255, -1)
    # masked = cv2.bitwise_and(pic, pic, mask=mask)
    bw_pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    gauss_bw_pic = cv2.GaussianBlur(bw_pic, (15, 15), 0)
    canny_gauss_bw_pic = cv2.Canny(gauss_bw_pic, 50, 70)

    # use the cv function called HoughCircles to detect circles and output those lines
    detected_circles = cv2.HoughCircles(canny_gauss_bw_pic, cv2.HOUGH_GRADIENT, 1, 20,
                                        param1=50, param2=20, minRadius=100,
                                        maxRadius=400)

    # make sure at least some circles were detected
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        # get the first parameters from the circle that is detected
        first_circle = detected_circles[0][1]

        # get the parameters for the center coordinates
        # and the radius of the first circle detected
        x, y, r = first_circle[0], first_circle[1], first_circle[2]

        # draw the circle for the circumference of the can
        cv2.circle(pic, (x, y), r, (70, 255, 133), 16)

        # draw the smaller circle for the center of the circle
        cv2.circle(pic, (x, y), 1, (70, 255, 133), 18)

        return pic
    else:
        print("no circle")
        return pic


# create video capture object
video = cv2.VideoCapture("rollingcan4.mov")

while video.isOpened():
    ret, frame = video.read()
    if ret:
        test = testdect(frame)
        cv2.imshow("Test", test)
        detected_frame = detection(frame)
        cv2.imshow("Detected Frame", detected_frame)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    else:
        break


video.release()
cv2.destroyAllWindows()

