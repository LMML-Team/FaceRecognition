# Camera

This provides a simple interface, via OpenCV, for configuring and utilizing a camera device, using Python

`camera` was created for the CogWorks 2017 summer program, in the [Beaver Works Summer Institute at MIT](https://beaverworks.ll.mit.edu/CMS/bw/bwsi). It was developed by [Ryan Soklaski](https://github.com/LLrsokl), the lead instructor of CogWorks 2017. 

## Installation Instructions
We will need to install OpenCV with the Python bindings so that we can access laptop cameras via our Python code. Follow the instructions for Windows and Mac.

### Windows Instructions (Python 3.{2-6})
Requires: Anaconda + Python 3.{2-6}, numpy, python-opencv

#### Method 1 (Recommended)
```shell
conda install -c conda-forge opencv
```

#### Method 2 (Back-Up Plan)
Installing python-opencv:

 1. Download the appropriate (32-bit or 64-bit) wheel package from 
   - http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv

 2. Navigate to the directory containing this .whl file, and simply run `pip install <whl-file-name>`
  > If you have multiple conda envs, make sure that the appropriate one is active when running the pip-install!

### Mac OS X Instructions (Python 3)
Requires: Anaconda + Python 3 (Tested on 3.{5-6}) + Homebrew

Installing opencv3:

- Ensure that Anaconda's python executable is the one being used (i.e. `which python` should yield `/path/to/anaconda/bin/python`)

- Update homebrew with `brew update`

- Install homebrew-science formulae with `brew tap homebrew/science`
  - This command allows opencv3 to be installed through homebrew

- Install opencv3 with homebrew using `brew install opencv3 --with-python3 --without-python --without-numpy --with-ffmpeg`

- Create a symbolic link of the compiled python binding to your Anaconda's site-package with the following commands for Python 3.5 and 3.6. **These paths need to be adjusted if you are installing opencv-python to a conda env other than root.**
  - (Python 3.5) `ln -s /usr/local/opt/opencv3/lib/python3.5/site-packages/cv2.cpython-35m-darwin.so /path/to/anaconda/lib/python3.5/site-packages/cv2.so`
  - (Python 3.6)`ln -s /usr/local/opt/opencv3/lib/python3.6/site-packages/cv2.cpython-36m-darwin.so /path/to/anaconda/lib/python3.6/site-packages/cv2.so`


Clone Camera, navigate to the resulting directory, and run

```shell
python setup.py develop
```

## Usage
Please see the camera tutorial notebookin this repo for details of how to configure your camera.

```python
%matplotlib notebook
from face_rec.camera import take_picture
import matplotlib.pyplot as plt
img_array = take_picture()

fig,ax = plt.subplots()
ax.imshow(img_array)
```
