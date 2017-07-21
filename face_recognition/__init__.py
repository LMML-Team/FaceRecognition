from camera import take_picture
import skimage.io as io
from time import sleep

from .config import *
from .detection import face_detection


def add_picture(filepath=None) :
    """

    Parameters
    -----------
    filepath: r"PATH" (optional)
        Analyzes a picture at the given filepath. If not file path is given, a picture is taken
    """
    if filepath is not None :
        img_array = io.imread(filepath)
    else :
        print("Please prepare to have your picture taken")
        sleep(2.5)
        img_array = take_picture()

    face_descriptors, face_borders = face_detection(img_array)
    names = get_names(face_descriptors)
    name_str, first_saved = format_names(names, face_descriptors)
    if first_saved :
        names = get_names(face_descriptors)
    show_image(img_array, face_borders, names)

    return name_str
