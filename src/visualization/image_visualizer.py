import cv2
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon


def show_image(
    image,
    bbox: Polygon = None,
    alpha: float = 0.2
):

    image_copy = image.copy()

    if bbox:

        def int_coords(coords):
            return np.array(coords).round().astype(np.int32)

        exterior = [int_coords(bbox.exterior.coords)]
        overlay = image_copy.copy()
        cv2.fillPoly(overlay, exterior, color=(255, 0, 0))
        cv2.addWeighted(overlay, alpha, image_copy, 1 - alpha, 0, image_copy)

    return plt.imshow(image_copy)
