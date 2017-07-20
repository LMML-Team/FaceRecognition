def descriptors(detections):
    """
    Calculates and returns descriptors for all detected faces in image
    
    Parameters
    -----------------------
    detections: List of detected faces
        
    Returns
    ----------------------
    
    """
    import skimage.io as io
    import numpy as np
    import dlib_models
    from dlib_models import load_dlib_models

    load_dlib_models()

    from dlib_models import models

    shape_predictor = models["shape predict"]

    descriptors = []

    face_rec_model = models["face rec"]
    for i in range(len(detections)):
        det = detections[i]
        shape = shape_predictor(img_array, det)
        descriptors[i] = np.array(face_rec_model.compute_face_descriptor(img_array, shape))

    return descriptors