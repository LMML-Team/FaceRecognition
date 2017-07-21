import pickle
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
    smallest_dist = 0
    for i, x in enumerate(iter(face_data)) :
        if len(face_data[x]) == 1 :
            dist = np.mean(np.sqrt(face_data[x]**2 + descriptor**2 - 2 * np.dot(face_data[x], descriptor)))
        else :
            dist = np.mean(np.sqrt(np.sum(face_data[x]**2, axis=1, keepdims=True) + descriptor**2 - 2 * np.dot(face_data[x], descriptor)))

        if i == 0 | dist < smallest_dist :
            smallest_dist = dist
            best_match = face_data[x]

    return best_match, face_data[best_match]
    # will return none if no best match found


def get_names(face_descriptors) :
    '''
    '''
    names = []
    for descriptor in face_descriptors :
        names.append(match_face(descriptor))
    return names


def format_names(names, face_descriptors) :
    '''
    '''
    if len(names) == 0 :
        return "No face is detected"
    elif len(names) == 1 :
        if names[0] is None :
            name = input("An unknown face is detected. If you would like to save this image, please enter the person's name. Otherwise, please enter 'None': ")
            if name.lower() is not 'none' :
                add_face(face_descriptors[0], name)
                save()
                return "Picture saved in database for %s" % (name)
            else :
                return "Picture not saved"
        else :
            should_save = input("%s is detected. Would you like you save this picture? Please enter 'Yes' or 'No': " % (names[0]))
            if should_save.lower() == "yes" :
                add_face(face_descriptors[0], names[0])
            elif should_save.lower() == "no" :
                return "Picture not saved"
            else :
                raise Exception("Input is not valid")
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

        return to_return


def show_image(img_array, face_borders, names) :
    '''
    '''
    # Create figure and axes
    fig, ax = plt.subplots(1)

    # Display the image
    ax.imshow(img_array)

    index = 0
    for border in face_borders:
        # Get borders for descriptor
        l, r, t, b = border

        # Create a Rectangle patch
        rect = patches.Rectangle((l, t), r - l, b - t, linewidth=1, edgecolor='y', facecolor='none')
        ax.annotate(names[index], (r, t), color='w', weight='bold', fontsize=10, ha='right', va='bottom')

        index += 1
        # Add the patch to the Axes
        ax.add_patch(rect)

    plt.show()
