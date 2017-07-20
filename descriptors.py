def descriptors(detections):
    shape_predictor = models["shape predict"]

    descriptors = []

    face_rec_model = models["face rec"]
    for i in range(len(detections)):
        det = detections[i]
        shape = shape_predictor(img_array, det)
        descriptors[i] = np.array(face_rec_model.compute_face_descriptor(img_array, shape))

    return descriptors