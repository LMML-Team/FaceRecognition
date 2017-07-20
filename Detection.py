def face_detection(filepath):
    import skimage.io as io
    import numpy as np
    import dlib_models
    from dlib_models import load_dlib_models

    load_dlib_models()

    from dlib_models import models

    img_array = io.imread(filepath)

    if np.size(img_array, 2) == 4:
        img_array = img_array[:, :, :4]

    face_detect = models["face detect"]

    upscale = 1

    detections = face_detect(img_array, upscale)
    detections = list(detections)

    borders(detections)
    descriptors(detections)

    return detections

