def borders(detections):
    for i in range(len(detections)):
        det = detections[i]
        l, r, t, b = det.left(), det.right(), det.top(), det.bottom()