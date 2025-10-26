import cv2

def detect_license_plate(gray_frame, cascade):
    """
    Detect number plates in a grayscale frame using Haar Cascade.
    Returns a list of rectangles: (x, y, w, h)
    """
    plates = cascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(25, 25)
    )
    return plates
