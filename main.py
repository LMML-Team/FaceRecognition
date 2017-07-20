import matplotlib.pyplot as plt
import matplotlib.patches as patches
from camera import test_camera, take_picture
from dlib_models import load_dlib_models

# this loads the dlib models into memory. You should only import the models *after* loading them.
# This does lazy-loading: it doesn't do anything if the models are already loaded.
load_dlib_models()

from dlib_models import models  # must be called after loading the models

img_array = take_picture()

face_detect = models["face detect"]

# Number of times to upscale image before detecting faces.
# When would you want to increase this number?
upscale = 1

detections = face_detect(img_array, upscale)  # returns sequence of face-detections
detections = list(detections)


# Create figure and axes
fig,ax = plt.subplots(1)

# Display the image
ax.imshow(img_array)

for rectangle in detections:
    det = rectangle # first detected face in image

    # bounding box dimensions for detection
    l, r, t, b = det.left(), det.right(), det.top(), det.bottom()

    # Create a Rectangle patch
    rect = patches.Rectangle((l, t), r-l, b-t ,linewidth=1,edgecolor='r',facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

plt.show()