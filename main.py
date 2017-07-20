import matplotlib.pyplot as plt
import matplotlib.patches as patches
from camera import test_camera, take_picture

from dlib_models import load_dlib_models

load_dlib_models()

from dlib_models import models  # must be called after loading the models

img_array = take_picture()

face_detect = models["face detect"]

upscale = 1

detections = face_detect(img_array, upscale)  # returns sequence of face-detections
detections = list(detections)

det = detections[0] # first detected face in image

# bounding box dimensions for detection
l, r, t, b = det.left(), det.right(), det.top(), det.bottom()

# Create figure and axes
fig,ax = plt.subplots(1)

# Display the image
ax.imshow(img_array)

print(l)
print(r)
print(t)
print(b)
# Create a Rectangle patch
rect = patches.Rectangle((l, t), r-l, b-t ,linewidth=1,edgecolor='r',facecolor='none')

# Add the patch to the Axes
ax.add_patch(rect)

plt.show()