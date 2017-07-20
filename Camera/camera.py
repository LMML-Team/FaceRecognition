from camera import test_camera

import matplotlib
from camera import take_picture
import matplotlib.pyplot as plt
img_array = take_picture()

fig,ax = plt.subplots()
ax.imshow(img_array)

# This will wait 0.5 seconds and then yield the active
# port-1 camera. Leaving the context releases the camera.
# You can read frames to take images or videos.
with use_camera(port=1, exposure=.5) as camera:
    # do stuff with camera
    # leaving this context releases camera