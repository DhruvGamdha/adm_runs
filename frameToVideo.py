# NOTE: use $VENV/gen/bin/python to run this script
import os
import cv2

# path to directory containing frames
baseDataDir = '/media/dgamdha/data/Dhruv/ISU/PhD/Projects/LEAP_HI/software/runs/adm_runs'

frame_dir = baseDataDir + '/tests/testing/cube/run11/frames/slice'
framerate = 15
videoName = "video_" + str(framerate) 
videoFormat = ".avi"
output_video = baseDataDir + '/' + videoName + videoFormat

# get list of frames in directory
frames = [f for f in os.listdir(frame_dir) if f.endswith('.png')]

# sort frames in ascending order
frames.sort()

# get dimensions of first frame
frame = cv2.imread(os.path.join(frame_dir, frames[0]))
height, width, layers = frame.shape

# create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc = cv2.VideoWriter_fourcc(*'H264')
video = cv2.VideoWriter(output_video, fourcc, framerate, (width, height), isColor=True)

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

os.chdir(baseDataDir)
command = 'ffmpeg -i ' + videoName + videoFormat + ' -vcodec libx264 -acodec aac ' + videoName + '.mp4'
print("Command  :",command)
os.system(command)

# Remove the avi file
os.remove(videoName + videoFormat)
 

