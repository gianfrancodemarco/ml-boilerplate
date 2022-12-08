import logging
import shutil

import requests
from tqdm import tqdm


def fetch_or_resume(url, filename):
    with open(filename, 'a+b') as f:
        logging.info(f"Downloading {url} in {filename}")
        
        headers = {}
        pos = f.tell()
        if pos:
            logging.info(f"Previous download found. Resuming...")
            headers['Range'] = f'bytes={pos}-'
        
        response = requests.get(url, headers=headers, stream=True)
        content_length = response.headers.get('content-length')
        
        if not content_length:
            logging.info("Download was already completed. Skipping.")
            return
        
        total_size = int(response.headers.get('content-length'))  
        for data in tqdm(iterable = response.iter_content(chunk_size = 1024), total = total_size//1024, unit = 'KB'):
            f.write(data)
        logging.info(f"Download complete.")


def download_image(url, dest):
    response = requests.get(url, stream=True)
    with open(dest, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response