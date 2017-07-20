import pickle
import os.path
import numpy as np

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
    if name not in face_data :
        face_data[name] = descriptor[0]
    else:
        face_data[name] = np.sqrt(face_data[name]**2 - descriptor[0]**2)

    save()


def match_face(descriptor) :
    best_match = max(iter(face_data), key=lambda x: np.sqrt(face_data[x]**2 - descriptor))
    return best_match
