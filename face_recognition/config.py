import pickle
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from .detection import borders

face_data = {}
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
    '''
    if name not in face_data :
        face_data[name] = descriptor
    else:
        face_data[name].append(descriptor)

    save()


def match_face(descriptor) :
    '''
    '''
    best_match = max(iter(face_data), key=lambda x: np.sqrt(np.sum(face_data[x]**2, axis=1, keepdims=True) + descriptor**2 - 2 * np.dot(face_data[x], descriptor)))
    return best_match


def return_names(face_descriptors) :
    '''
    '''
    if len(face_descriptors) == 0 :
        return "No face is detected"
    elif len(face_descriptors) == 1 :
        if face_descriptors[0] not in face_data :
            name = input("An unknown face is detected. If you would like to save this image, please enter the person's name. Otherwise, please enter 'None': ")
            if name is not None :
                add_face(face_descriptors[0], name)
                save()
                return "Picture saved in database for %s" % (name)
            else :
                return "Picture not saved"
        else :
            name = match_face(face_descriptors[0])
            should_save = input("%s is detected. Would you like you save this picture? Please enter 'Yes' or 'No': " % (name))
            if should_save.lower() == "yes" :
                add_face(face_descriptors[0], name)
            elif should_save.lower() == "no" :
                return "Picture not saved"
            else :
                raise Exception("Input is not valid")
    else :
        names = []
        to_return = ""
        for descriptor in face_descriptors :
            names.append(match_face(descriptor))
            if len(names) < len(face_descriptors) - 1 :
                to_return += names[-1] + ", "
            else :
                to_return += "and " + names[-1]
        return to_return + " are detected"


def show_image(img_array, face_descriptors) :
    '''
    '''
    # Create figure and axes
    fig, ax = plt.subplots(1)

    # Display the image
    ax.imshow(img_array)

    for descriptor in face_descriptors:
        # Get borders for descriptor
        l, r, t, b = borders(descriptor)

        # Create a Rectangle patch
        rect = patches.Rectangle((l, t), r - l, b - t, linewidth=1, edgecolor='r', facecolor='none')

        # Add the patch to the Axes
        ax.add_patch(rect)

    plt.show()
