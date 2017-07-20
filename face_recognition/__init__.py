import camera
import skimage.io as io

from config import *


def import_picture(filepath) :
    """
    """
    img_array = io.imread(filepath)
    face_borders, face_descriptors = face_detection(img_array)

    if len(face_descriptors) == 0 :
        return "No face is detected"
    elif len(face_descriptors) == 1 :
        if face_descriptor[0] not in face_data :
            name = input("An unknown face is detected. If you would like to save this image, please enter the person's name. Otherwise, please enter 'None': ")
            if name is not None :
                add_face(face_descriptor[0], name)
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
            if len(names) < len(face_descriptors)-1 :
                to_return += names[-1] + ", "
            else :
                to_return += "and " + names[-1]
        return to_return + " are detected"


def take_picture() :
    """
    """
    pass
