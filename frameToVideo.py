# NOTE: use $VENV/gen/bin/python to run this script
# Look at batch_frameToVideo.sh for running this script in batch mode
import os
import cv2
import pathlib as pl
import argparse

parser = argparse.ArgumentParser(description='Convert frames to video')
parser.add_argument('--runDirPath', type=str, help='Path to the run directory')
parser.add_argument('--frameDirName', type=str, help='Name to the frame directory')
parser.add_argument('--framerate', type=int, default=15, help='Frame rate of the video')
parser.add_argument('--lastFrameCopyCount', type=int, default=10, help='Number of times to copy the last frame')
args = parser.parse_args()

runDirPath          = pl.Path(args.runDirPath)
framerate           = args.framerate
lastFrameCopyCount  = args.lastFrameCopyCount
videoName           = args.frameDirName + "_" + str(framerate)
videoFormat         = ".avi"
frame_dir           = runDirPath / args.frameDirName
output_video        = runDirPath / (videoName + videoFormat)

# get list of frames in directory
frames = [f for f in os.listdir(frame_dir) if f.endswith('.png')]
frames.sort()

# Copy the last frame multiple times
for i in range(lastFrameCopyCount):
    frames.append(frames[-1])

# get dimensions of first frame
frame = cv2.imread(os.path.join(frame_dir, frames[0]))
height, width, layers = frame.shape

# create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc = cv2.VideoWriter_fourcc(*'H264')
video = cv2.VideoWriter(str(output_video), fourcc, framerate, (width, height), isColor=True)

# loop through frames and add to video
for frame_name in frames:
    frame = cv2.imread(os.path.join(frame_dir, frame_name))
    frame = cv2.resize(frame, (width, height))
    video.write(frame)
    # cv2.imshow('frame', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# release resources and close windows
cv2.destroyAllWindows()
video.release()

# os.chdir(baseDataDir)
os.chdir(runDirPath)
command = 'ffmpeg -i ' + videoName + videoFormat + ' -vcodec libx264 -acodec aac ' + videoName + '.mp4'
print("Command  :",command)
os.system(command)

# Remove the avi file
os.remove(videoName + videoFormat)
 

