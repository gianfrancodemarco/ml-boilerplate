import copy
import logging
import math
import random
import shutil
from typing import List, Tuple

import requests
from shapely.affinity import translate
from shapely.geometry import Polygon
from tqdm import tqdm


def fetch_or_resume(url, filename):
    with open(filename, 'a+b') as f:
        logging.info(f"Downloading {url} in {filename}")

        headers = {}
        pos = f.tell()
        if pos:
            logging.info("Previous download found. Resuming...")
            headers['Range'] = f'bytes={pos}-'

        response = requests.get(url, headers=headers, stream=True)
        content_length = response.headers.get('content-length')

        if not content_length:
            logging.info("Download was already completed. Skipping.")
            return

        total_size = int(response.headers.get('content-length'))
        for data in tqdm(iterable=response.iter_content(chunk_size=1024), total=total_size//1024, unit='KB'):
            f.write(data)
        logging.info("Download complete.")


def download_image(url, dest):
    response = requests.get(url, stream=True)
    with open(dest, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def sort_2d_points(
    points,
    centre=None,
    clockwise=True
):
    """
    https://stackoverflow.com/questions/69100978/how-to-sort-a-list-of-points-in-clockwise-anti-clockwise-in-python

    Sorts a list of 2d points [(x1,y1), ...] in a clockwise order wrt the center.
    If the center is null, it is computed as the centroid of the points
    """

    if centre:
        centre_x, centre_y = centre
    else:
        centre_x, centre_y = sum(
            [x for x, _ in points])/len(points), sum([y for _, y in points])/len(points)

    if clockwise:
        def key_fun(i):
            return -angles[i]
    else:
        def key_fun(i):
            return angles[i]

    angles = [math.atan2(y - centre_y, x - centre_x) for x, y in points]
    indices = sorted(range(len(points)), key=key_fun)
    sorted_points = [points[i] for i in indices]
    return sorted_points


def get_random_translated_polygon_in_boundary_and_not_overlapping(
    polygon: Polygon,
    destination_width: int,
    destination_height: int,
    existing_polygons: List[Polygon],
    max_tries = 100
) -> Tuple[Polygon, bool]:

    """
    Translates randomly a polygon in a space, so that:
        - the polygon stays inside max_x and max_y 
        - the polygon doesn't overlap with any of overlappingsstaying into the max_x and max_y boundary.

    The overlapping is checked by brute forcing the polygon translation until a not overlapping is found

    Returns a tuple:
    - the translated polygon
    - if it has succeded generating a non overlapping polygon or not
    """

    translated_polygon = copy.copy(polygon)

    min_x, min_y, max_x, max_y = polygon.bounds
    
    from_border_x_to_polygon = int(min_x)
    from_polygon_to_border_x = int(destination_width - max_x)
    from_border_y_to_polygon = int(min_y)
    from_polygon_to_border_y = int(destination_height - max_y)

    # TODO: Here if we are translating up, we could scale the polygon down a bit
    # If we are scaling down, we could scale the polygon up a bit

    collision = True
    current_try = 0
    
    while collision and current_try < max_tries:
        
        collision = False
        
        translate_x = random.randint(-from_border_x_to_polygon, from_polygon_to_border_x)
        translate_y = random.randint(-from_border_y_to_polygon, from_polygon_to_border_y)
        translated_polygon = translate(polygon, translate_x, translate_y)

        for existing_polygon in existing_polygons:
            if translated_polygon.intersects(existing_polygon):
                logging.warning(f"Failed try number {current_try} to generate a non-overlapping translation. Max tries: {max_tries}")
                collision = True
                current_try = current_try + 1
    
    return (translated_polygon, not collision)
