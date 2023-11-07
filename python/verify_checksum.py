import os, sys, logging, random
import multiprocessing as mp
import hashlib
from glob import glob
from tqdm import tqdm
from urllib.request import urlretrieve
import logging

logging.basicConfig(level='WARNING')

BASE_URL = 'https://data.binance.vision/'
LOCAL_DIR = 'g:/i_download/binance/'


def sh256sum(fname):
    with open(fname, "rb") as f:
        res = hashlib.sha256(f.read())
    return res.hexdigest()


def verify_checksum(file, redownload=True):
    try:
        file_checksum = file + '.CHECKSUM'
        if (not os.path.exists(file_checksum)) and redownload:
            url_checksum = file_checksum.replace(LOCAL_DIR, BASE_URL).replace('\\', '/')
            logging.info(f"downloading {url_checksum}")
            urlretrieve(url_checksum, file_checksum)
        checksum = open(file_checksum, 'rb').read().decode().split(' ')[0]
        if sh256sum(file) == checksum:
            logging.info(f"checksum verified {file}")
        elif redownload:
            logging.warning(f"redownloading {file}")
            download_file(file)
        else:
            logging.error(f"checksum failed {file}")
    except Exception as e:
        logging.exception(f"error processing {file} {e}")
    return file


def download_file(file):
    url_source = file.replace(LOCAL_DIR, BASE_URL).replace('\\', '/')
    logging.info(f"downloading {url_source}")
    urlretrieve(url_source, file)
    return file


def main():
    dir_pattern = os.path.join(LOCAL_DIR, 'data/*/*/daily/*/*/*.zip')
    logging.info(f"searching file patten {dir_pattern}")
    list_file = glob(dir_pattern)
    logging.info(f"total file count={len(list_file)}")
    random.shuffle(list_file)
    with mp.Pool(8) as p:
        r = list(tqdm(p.imap(verify_checksum, list_file), total=len(list_file)))
    # for file in tqdm(list_file):
    #     try:
    #         verify_checksum(file, redownload=True)
    #     except Exception as e:
    #         logging.exception(f"error processing {file} {e}")
    return


if __name__ == "__main__":
    main()
