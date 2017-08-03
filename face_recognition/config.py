import pickle
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import OrderedDict

face_data = OrderedDict()
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "face_data.pickle"), 'rb') as f:
    face_data = pickle.load(f)


def save() :
    '''
    Saves face_data to a .pickle file
    '''
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "face_data.pickle"), 'wb') as f:
        pickle.dump(face_data, f, pickle.HIGHEST_PROTOCOL)


def add_face(descriptor, name) :
    '''
    Adds descriptor and name to face_data, or averages current descriptor for name

    Parameters
    -----------
    descriptor: ndarray
        descriptor for face, returned by face_recognition.detections.face_detection
    name: str
        name of person to be stored in database with given descriptor
    '''
    if name not in face_data :
        face_data[name] = descriptor
    else:
        face_data[name] = (face_data[name] + descriptor) / 2

    save()


def remove_person(name) :
    '''
    Removes name's descriptor and name from database

    Parameters
    -----------
    name: str
        name of person to be removed
    '''
    if name not in face_data :
        return "%s is not in the database" % (name)
    else :
        del face_data[name]
        save()


def list_names() :
    '''
    Lists names of all people in database
    '''
    return list(face_data.keys())


def match_face(descriptor) :
    '''
    Finds the face descriptor from database that best matches descriptor

    Parameters
    -----------
    descriptor: ndarray
        descriptor of detected face
    '''
    descriptors = np.vstack(list(face_data.values()))
    dist = np.sqrt(np.abs(np.sum(descriptors**2, axis=1) + np.sum(descriptor**2) - 2 * np.dot(descriptors, descriptor)))
    dist_index = np.argmin(dist)
    print(dist)

    if dist[dist_index] > .3 :
        best_match = None
        best_descriptor = None
    else :
        best_match = list(face_data.keys())[dist_index]
        best_descriptor = face_data[best_match]

    return best_match, best_descriptor


def get_names(face_descriptors) :
    '''
    Returns list of names corresponding to descriptors

    Parameters
    -----------
    face_descriptors: iterable of ndarrays
        iterable of face descriptors detected in a photo

    Returns
    --------
    names: list of str
        list of names best matching face descriptors
    '''
    names = []
    for descriptor in face_descriptors :
        names.append(match_face(descriptor)[0])
    return names


def format_names(names, face_descriptors, alexa) :
    '''
    Returns formatted string of user's names

    Parameters
    -----------
    names: list of str
        list of names of people in picture
    face_descriptors: iterable of ndarrays
        iterable of face descriptors detected in a photo
    alexa: boolean
        whether to prompt user to save photo or enter new name
    '''
    if len(names) == 0 :
        return "No face is detected", False
    elif len(names) == 1 :
        if names[0] is None :
            if alexa == True :
                return "An unknown face is detected", False
            else :
                name = input("An unknown face is detected. If you would like to save this image, please enter the person's name. Otherwise, please enter 'None': ")
                if name.lower() != 'none' :
                    add_face(face_descriptors[0], name)
                    save()
                    return "Picture saved in database for %s" % (name), True
                else :
                    return "Picture not saved", False
        else :
            if alexa == True :
                return "%s is detected" % (names[0]), False
            else :
                should_save = input("%s is detected. Would you like you save this picture? Please enter 'Yes' or 'No': " % (names[0]))
                if should_save.lower() == "yes" :
                    add_face(face_descriptors[0], names[0])
                    return "Picture was saved", False
                elif should_save.lower() == "no" :
                    return "Picture not saved", False
                else :
                    raise Exception("Input is not valid")
    elif len(names) == 2 :
        nones = names.count(None)
        to_return = ", ".join(filter(None, names))

        if nones > 0 :
            if nones == 1 :
                to_return = to_return + " and 1 unknown person are detected"
        else :
            split = to_return.rpartition(", ")
            to_return = split[0] + " and " + split[2] + " are detected"

        return to_return, False
    else :
        nones = names.count(None)
        to_return = ", ".join(filter(None, names))

        if nones > 0 :
            if nones == 1 :
                to_return = to_return + ", and 1 unknown person are detected"
            else :
                to_return = to_return + ", and %s unknown people are detected" % nones
        else :
            split = to_return.rpartition(", ")
            to_return = split[0] + split[1] + "and " + split[2] + " are detected"

        return to_return, False


def show_image(img_array, face_borders, names) :
    '''
    Shows the image with faces boxed and labeled

    Parameters
    -----------
    img_array: np.array
        matrix of the image information
    face_borders: iterable of ints
        iterable of box coordinates for all faces recognized
    names: iterable of strs
        iterable of all names of faces recognized

    '''
    # Create figure and axes
    fig, ax = plt.subplots(1)

    # Display the image
    ax.imshow(img_array)

    for i, border in enumerate(face_borders):
        # Get borders for descriptor
        l, r, t, b = border

        # Create a Rectangle patch
        rect = patches.Rectangle((l, t), r - l, b - t, linewidth=1, edgecolor='y', facecolor='none')
        if names[i] is not None :
            ax.annotate(names[i], (r, t), color='w', weight='bold', fontsize=10, ha='right', va='bottom')

        # Add the patch to the Axes
        ax.add_patch(rect)

    plt.show()


# work in progress
def rgb_to_hsv(rgb_img) :
    '''
    Parameters
    -----------
    rgb_img: numpy array of shape NxMx3
    '''
    rgb_prime = rgb_img / 255
    rgb_max_index = np.argmax(rgb_img, axis=2)
    Cmax = np.amax(rgb_prime, axis=2)
    Cmin = np.amin(rgb_prime, axis=2)
    delta = Cmax - Cmin
    hue = np.zeros(rgb_img.shape)
    sat = np.zeros(rgb_img.shape)

    # gets indices of maximum prime colors
    r_prime_indices = list(zip(np.where(rgb_max_index == 0 & delta != 0, rgb_prime)))
    b_prime_indices = list(zip(np.where(rgb_max_index == 1 & delta != 0, rgb_prime)))
    g_prime_indices = list(zip(np.where(rgb_max_index == 2 & delta != 0, rgb_prime)))
    delta_zeros = list(zip(np.where(delta == 0)))
    Cmax_zeros = list(zip(np.where(Cmax == 0)))
    Cmax_nonzeros = list(zip(np.where(Cmax != 0)))

    hue[delta_zeros] = 0
    hue[r_prime_indices] = 60 * (rgb_prime[g_prime_indices] - rgb_prime[b_prime_indices]) / delta % 6
    hue[g_prime_indices] = 60 * (rgb_prime[b_prime_indices] - rgb_prime[r_prime_indices]) / delta + 2
    hue[b_prime_indices] = 60 * (rgb_prime[r_prime_indices] - rgb_prime[g_prime_indices]) / delta + 4

    sat[Cmax_zeros] = 0
    sat[Cmax_nonzeros] = delta[Cmax_nonzeros] / Cmax[Cmax_nonzeros]

    hsv_img = np.dstack(hue, sat, Cmax)

    return hsv_img


def complementary_color(hsv_img) :
    """
    """
    hue = hsv_img[0]
    hue_greater_180 = list(zip(np.where(hue > 180)))
    hue_less_eq_180 = list(zip(np.where(hue <= 180)))

    comp_color_hsv = np.copy(hsv_img)
    comp_color_hsv[0][hue_greater_180] = hue[hue_greater_180] - 180
    comp_color_hsv[0][hue_less_eq_180] = hue[hue_less_eq_180] + 180

    return comp_color_hsv
