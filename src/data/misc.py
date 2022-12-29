import logging
import math
import shutil

import requests
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
    centre = None,
    clockwise = True
    ):
    """
    https://stackoverflow.com/questions/69100978/how-to-sort-a-list-of-points-in-clockwise-anti-clockwise-in-python

    Sorts a list of 2d points [(x1,y1), ...] in a clockwise order wrt the center.
    If the center is null, it is computed as the centroid of the points
    """

    if centre:
        centre_x, centre_y = centre
    else:
        centre_x, centre_y = sum([x for x,_ in points])/len(points), sum([y for _,y in points])/len(points)

    if clockwise:
        def key_fun(i):
            return -angles[i]
    else:
        def key_fun(i):
            return angles[i]
    
    angles = [math.atan2(y - centre_y, x - centre_x) for x,y in points]
    counterclockwise_indices = sorted(range(len(points)), key=key_fun)
    counterclockwise_points = [points[i] for i in counterclockwise_indices]
    return counterclockwise_points
