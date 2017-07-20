""" Provides utilities for configuring your device's camera, and using it.

    'port' should be an integer, typically 0. This indicates which
    camera-device should be used. For the Surface Pro 3, for example,
    you need to set this to 1 in order to use the screen-side camera.

    'exposure' is the time (seconds) for which the camera is active before
    taking the photo. If your photo is too dark, try increasing this time. """

import configparser
import os
import cv2
from contextlib import contextmanager
import matplotlib.pyplot as plt
from pathlib import Path

_path = Path(os.path.dirname(os.path.abspath(__file__))) / 'config.ini'


def _load_config(msg=False):
    """ Returns the saved device from config.ini or a dictionary
        of default values: {"port": 0, "exposure": 0.1}

        Returns
        -------
        Union[dict, None]
            {name : device name,
             index: device index from config prompt}"""
    config = configparser.ConfigParser()
    # This returns an empty array if no config file was found
    if config.read(str(_path)) != []:
        port = int(config['camera device']["port"])
        exposure = float(config['camera device']["exposure"])
        return {"port": port, "exposure": exposure}
    else:
        if msg:
            print("No camera config found, using defaults\n\t port=0, exposure=0.7")
        return {"port": 0, "exposure": 0.1}


def save_camera_config(port=None, exposure=None):
    """ Save the specified port and exposure values. If `None` is specified for a config-value,
        the current saved value (or default value) will be used.

        Parameters
        ----------
        port : Optional[int], (default=0)
            An integer, typically 0. This indicates which camera-device should be used.

        exposure : Optional[float], (default=0.1)
            The time (seconds) for which the camera is active before taking the photo.
            If your photo is too dark, try increasing this time."""
    msg = port is None and exposure is None
    conf = _load_config(msg)
    port = conf["port"] if port is None else port
    exposure = conf["exposure"] if exposure is None else exposure
    assert isinstance(port, int)
    assert isinstance(exposure, (float, int))
    config = configparser.ConfigParser()
    config['camera device'] = {'port': str(port),
                               'exposure': str(exposure)}
    with _path.open(mode='w') as configfile:
        config.write(configfile)
    print("Configuration saved: \n\tport: {}, exposure {} (sec)".format(port, exposure))


@contextmanager
def use_camera(port=None, exposure=None):
    """ A context manager for a `cv2.VideoCapture()` instance. An amount of time,
        `exposure`, is waited before yielding the camera device to the user.

        Leaving the context releases the camera.

        Parameters
        ----------
        port : Optional[int], (default=0)
            An integer, typically 0. This indicates which camera-device should be used.

        exposure : Optional[float], (default=0.1)
            The time (seconds) for which the camera is active before taking the photo.
            If your photo is too dark, try increasing this time.

        Yields
        ------
        cv2.VideoCapture
            The video-capture instance of the specified camera."""
    import time
    msg = port is None and exposure is None
    conf = _load_config(msg)
    port = conf["port"] if port is None else port
    exposure = conf["exposure"] if exposure is None else exposure
    assert isinstance(port, int)
    assert isinstance(exposure, (float, int))
    try:
        camera = cv2.VideoCapture(port)
        time.sleep(exposure)  # If you don't wait, the image will be dark
        yield camera
    finally:
        camera.release()


def test_camera(port=None, exposure=None):
    """ Take and display a picture using the specified configuration. If `None` is
        provided for a config value, the saved (or default) configuration
        value will be used.

        Parameters
        ----------
        port : Optional[int], (default=0)
            An integer, typically 0. This indicates which camera-device should be used.

        exposure : Optional[float], (default=0.1)
            The time (seconds) for which the camera is active before taking the photo.
            If your photo is too dark, try increasing this time.

        Returns
        -------
        Tuple[matplotlib.Fig, matplotlib.Axis, numpy.ndarray]
            The matplotlib figure and axis objects for the displayed picture, and the RGB-valued numpy array.
        """

    conf = _load_config()
    port = conf["port"] if port is None else port
    exposure = conf["exposure"] if exposure is None else exposure
    print("Testing port: {}, exposure: {}(sec)".format(port, exposure))

    with use_camera(port, exposure) as camera:
        return_value, image = camera.read()  # return (H, W, [BGR]). NOT RGB!
    image = image[..., ::-1]  # BGR -> RGB
    fig, ax = plt.subplots()
    ax.imshow(image)
    return fig, ax, image


def take_picture():
    """ Take a picture and return the (H, W, 3) array of RGB values.

        Returns
        -------
        numpy.ndarray, shape=(H, W, 3)
            RGB values. """
    with use_camera() as camera:
        return_value, image = camera.read()  # return (H, W, [BGR]). NOT RGB!
    return image[..., ::-1]
