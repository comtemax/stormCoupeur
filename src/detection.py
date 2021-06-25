import cv2
import time


INTER_FRAME_DELAY = 0.2 #delay between each frame. An increased delay means slower motion in the video
BEFORE_LIGHTNING_DELAY = 3 #delay in seconds to let before the lightning to smoother the clip (and not get the flash right at video opening)
BRIGHTNESS_TOLERANCE_VALUE = 11 # used arbitrarily, it seems to detect quite nicely the thunder for the video it was tested on
HSV_MAX_TOLERANCE = 100 #brightest point of the picture. Had false negative at 10.10 mean value and 130 max value so try to tweek it with max values

def init():
    return 0

def extract_clips(path="../data/VID_20210620_012219.mp4"):
    # get the video flux
    cap = cv2.VideoCapture(path)
    #movement detection
    #object_detector = cv2.createBackgroundSubtractorMOG2()
    extracted_sequences = 0
    seq_nb = 0

    frames_to_extract = process_video(cap)
    print(frames_to_extract)
    cap.release()
    cv2.destroyAllWindows()
    return

def process_video(cap):
    index = 0
    extracted_frames = 0
    frames_to_extract = []
    brightest_frames = []
    while True:
        ret, frame = cap.read()
#        print(f"{ret}{cap}")
        if ret is False:
            print("No more frames to grab. Closing")
            break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # get the mean of the Value (HSV's 3rd component)
        hsv_mean = hsv[...,2].mean()
        # get the max of the Value (HSV's 3rd component) to distinguish lightnings
        hsv_max = hsv[...,2].max()
        hsv_min = hsv[...,2].min()


        if (hsv_mean > BRIGHTNESS_TOLERANCE_VALUE or hsv_max > HSV_MAX_TOLERANCE):
            print(f"THUNDER !!! frameIndex = {index} -- HSV mean {hsv_mean}     min {hsv_min}       max {hsv_max}")
            frames_to_extract.append(index) #could be replaced by THE ACTUAL FRAME stocked in videoSTREAM to finally ultimately write it
            extracted_frames += 1
#todo change arbitrarily set var
            if hsv_mean > 55:
                brightest_frames.append(index)
                print(f"Addind {index} with {hsv_mean}")
            #slomo the thunder
            time.sleep(0.2)
        else:
            print(f"frameIndex = {index} -- HSV mean {hsv_mean}     min {hsv_min}       max {hsv_max}")
        cv2.imshow("Thunder", frame)
        cv2.imshow("grayscale",hsv[...,2])
        #pause on a certain frame
        # if index == 102:
        #     print("PAUSED")
        #     cv2.waitKey(-1) #wait until any key is pressed

        # KEYBOARD INPUT HANDLING
        key = cv2.waitKey(2)
        if key == 27:
            print("Escaped")
            break
        #TEMPORARY PAUSE logic
        if key == ord(' '):
            print("PAUSED")
            cv2.waitKey(-1) #wait until any key is pressed

        index += 1
    return frames_to_extract

def main():
    extract_clips()

if __name__ == "__main__":
    main()

#LOGIC TO IMPLEMENT
#2 passes on the video.
# firt to get timestamps of lightnings
# the other to extract the clips at start_timestamp - x sec (if start_timestamp - x > video_start) and stop_timestamp

#save these clips in video_name new folder, extend each clip with the index of lightnings (1st, 2nd ...)
# each clip could be provided with a thumbnail at the brightest peak of the lightning


            # was used to draw contours of moving parts but not needed
            #obj detector
            #mask = object_detector.apply(frame)
            #contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # if not frame is None:
            #     totaldrawn = 0
            # for cnt in contours:
            #     area = cv2.contourArea(cnt)
            #     if area > 100:
            #         totaldrawn += 1
            #         cv2.drawContours(frame, [cnt], -1, (0, 25, 0), 1)
            # if totaldrawn > 0 and index > 0:
            # slomo the thunder
