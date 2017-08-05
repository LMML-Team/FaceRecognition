from camera import take_picture
import skimage.io as io
from time import sleep

from .config import *
from .detection import face_detection
from .whispers import Node, Graph


def add_picture(filepath=None, alexa=False) :
    """
    Adds picture to database of images

    Parameters
    -----------
    filepath: r"PATH" (optional)
        analyzes a picture at the given filepath. if no file path is given, a picture is taken
    alexa: boolean
        whether to prompt user and show picture (false) or simply return string (true)
    """
    if filepath is not None :
        img_array = io.imread(filepath)
    else :
        print("Please prepare to have your picture taken")
        sleep(2.5)
        img_array = take_picture()

    face_descriptors, face_borders = face_detection(img_array)
    names = get_names(face_descriptors)
    name_str, first_saved = format_names(names, face_descriptors, alexa)
    if first_saved :
        names = get_names(face_descriptors)
    if not alexa :
        show_image(img_array, face_borders, names)

    return name_str


def sort_pictures(directory):
    """
    Sorts directory of photos by people in photo

    Parameters
    -----------
    directory: r"PATH"
        path to directory of photos to sort
    """
    lab = 0
    nodes = []

    for file in os.listdir(directory):
        if file.endswith((".jpg", ".png")):
            img_array = io.imread(os.path.join(directory, file))
            descriptor = np.mean(face_detection(img_array)[0], axis=0)
            filename = os.fsdecode(file)
            nodes.append(Node(lab, descriptor, file_path = os.path.join(directory, filename)))
            lab += 1
        else:
            continue

    graph = Graph(nodes)
    graph.set_all_neighbors()
    graph.build_graph()
    graph.sort_pictures()
