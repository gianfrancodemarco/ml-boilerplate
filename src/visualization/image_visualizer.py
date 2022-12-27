import cv2
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon

def show_image(
    image,
    bbox: Polygon = None,
    alpha: float = 0.2
):    
    if bbox:
        int_coords = lambda x: np.array(x).round().astype(np.int32)
        exterior = [int_coords(bbox.exterior.coords)]
        overlay = image.copy()
        cv2.fillPoly(overlay, exterior, color=(255, 0, 0))
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
        
    return plt.imshow(image)