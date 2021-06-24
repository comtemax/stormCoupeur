import cv2
import time

cap = cv2.VideoCapture("../data/VID_20210620_012219.mp4")

#obj detect
object_detector = cv2.createBackgroundSubtractorMOG2()

INTER_FRAME_DELAY = 0.2 #delay between each frame. An increased delay means slower motion in the video
BEFORE_LIGHTNING_DELAY = 3 #delay in seconds to let before the lightning to smoother the clip (and not get the flash right at video opening)
BRIGHTNESS_TOLERANCE_VALUE = 11
index = 0


while True:
    ret, frame = cap.read()
    if ret is False:
        break

    #obj detector
    mask = object_detector.apply(frame)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_mean = hsv[...,2].mean()

#    print(f"hsv : {hsv}")

    if (hsv_mean > BRIGHTNESS_TOLERANCE_VALUE):
        print("THUNDER !!!")
        print(f"HSV mean {hsv_mean}")
        print(f"HSV peak spot {hsv[...,2].max()}")


    if not frame is None:
        totaldrawn = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:
                totaldrawn += 1
                cv2.drawContours(frame, [cnt], -1, (0, 25, 0), 1)

        #slomo the thunder
        if totaldrawn > 0 and index > 0:
            print("SLOWING THE SH*T DOWN")
            time.sleep(0.1)

        cv2.imshow("Thunder", frame)
#        cv2.imshow("HSV", hsv)
        cv2.imshow("grayscale",hsv[...,2])

        # KEYBOARD INPUT HANDLING
        key = cv2.waitKey(20)
        #echap
        if key == 27:
            print("Escaping")
            break
        #TEMPORARY PAUSE logic
        if key == ord(' '):
            print("PAUSED")
            cv2.waitKey(-1) #wait until any key is pressed

        index += 1

cap.release()
cv2.destroyAllWindows()


#LOGIC TO IMPLEMENT
#2 passes on the video.
# firt to get timestamps of lightnings
# the other to extract the clips at start_timestamp - x sec (if start_timestamp - x > video_start) and stop_timestamp

#save these clips in video_name new folder, extend each clip with the index of lightnings (1st, 2nd ...)
# each clip could be provided with a thumbnail at the brightest peak of the lightning
