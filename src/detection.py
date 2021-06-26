import cv2
from datetime import datetime
import time
import sys
import os

BASE_INTER_FRAME_DELAY = 0.002 #delay between each frame. An increased delay means slower motion in the video
SLOMO_INTER_FRAME_DELAY = 0.2 #delay between each frame. An increased delay means slower motion in the video
BEFORE_LIGHTNING_FRAMES = 5 #delay in seconds to let before the lightning to smoother the clip (and not get the flash right at video opening)
BRIGHTNESS_TOLERANCE_VALUE = 11 # used arbitrarily, it seems to detect quite nicely the thunder for the video it was tested on
HSV_MAX_TOLERANCE = 100 #brightest point of the picture. Had false negative at 10.10 mean value and 130 max value so try to tweek it with max values

def init():
    return 0

def extract_clips(path):
    # get the video flux
    cap = cv2.VideoCapture(path)
    if (cap.isOpened() == False):
        print(f"Error, failed to open {path} video")
        return

    brightest_frames = []
    frames_to_extract = process_video(cap, brightest_frames)
    #Clip is 1 sequence itself + the discontinuities
    nb_sequences = 1 + check_discontinuities(frames_to_extract)

    #done to reset the iterator if the videocapture object
    cap.release()
    cap = cv2.VideoCapture(path)
    #pass again the video to extract to determined images
    frame_extraction(cap, frames_to_extract, nb_sequences, brightest_frames)
    print(f"fte{frames_to_extract}, len fte {len(frames_to_extract)}\n nbseq {nb_sequences}, brightest_frames {brightest_frames}")
    cap.release()
    cv2.destroyAllWindows()
    return

def check_discontinuities(lst):
    if (len(lst) < 1):
        return 0
    disc = 0
    for i, val in enumerate(lst):
        # if next elem - current elem != 1, they are not consecutive
        if i + 1 < len(lst) :
            if lst[i + 1] - lst[i] != 1:
                disc += 1
    return disc

def frame_extraction(cap, frames_to_extract, nb_sequences, brightest_frames):
    vid_width = int(cap.get(3))
    vid_height = int(cap.get(4))
    vid_fps = cap.get(cv2.CAP_PROP_FPS)
    outputs = []
    output_dirname = f"output-{datetime.now().replace(microsecond=0)}"
    try:
        #codec for the videoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        for i in range(nb_sequences):
            outfoldername = f"{output_dirname}/thunder-{i}"
            os.makedirs(outfoldername)
            outputs.append(cv2.VideoWriter(f"{outfoldername}/thunder.avi", fourcc, vid_fps, (vid_width, vid_height)))
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
                #on error ...

    frameIndex = 0
    seq_nb = 0
    print(f"Starting extract job with {frames_to_extract}")
    while True:
        ret, frame = cap.read()
        if ret is False:
            print("No more frames to grab. Closing")
            break
        #a bit clunky if we have a fiew frames to extract, due to arbitrarily set NB_FRAMES_BEFORE_THUNDER
        if (frameIndex in frames_to_extract or frameIndex + BEFORE_LIGHTNING_FRAMES in frames_to_extract):
            outputs[seq_nb].write(frame)
            print(f"Wrote {frameIndex} frame in {outputs[seq_nb]}")
        if frameIndex in brightest_frames:
            #save the picture alongside the video
            print(f"Saving {output_dirname}/thunder-{seq_nb}/thunder-{frameIndex}.jpeg")
            try:
                cv2.imwrite(f"{output_dirname}/thunder-{seq_nb}/thunder-{frameIndex}.jpeg", frame)
            except:
                print("Oops!", sys.exc_info()[0], "occurred.")

        if frameIndex in frames_to_extract and frameIndex+1 not in frames_to_extract:
            seq_nb += 1
        frameIndex += 1

    for i in range(nb_sequences):
        print(f"releasing {i} - {outputs[i]}")
        outputs[i].release()


def process_video(cap, brightest_frames):
    index = 0
    extracted_frames = 0
    frames_to_extract = []
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

#tmp speedup
        time.sleep(BASE_INTER_FRAME_DELAY)

        if (hsv_mean > BRIGHTNESS_TOLERANCE_VALUE or hsv_max > HSV_MAX_TOLERANCE):
            print(f"THUNDER !!! frameIndex = {index} -- HSV mean {hsv_mean}     min {hsv_min}       max {hsv_max}")
            frames_to_extract.append(index) #could be replaced by THE ACTUAL FRAME stocked in videoSTREAM to finally ultimately write it
            extracted_frames += 1
#todo change arbitrarily set var
            if hsv_mean > 55:
                brightest_frames.append(index)
                print(f"Addind {index} with {hsv_mean}")
            #SHOULD BE SLOMO_INTER_FRAME_DELAY
            time.sleep(BASE_INTER_FRAME_DELAY)
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
    videopath = "../data/VID_20210620_012219.mp4"
    extract_clips(videopath)

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
