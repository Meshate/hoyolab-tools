import time
import requests
from utils import log

def cookie_to_dict(cookie):
    if cookie and '=' in cookie:
        cookie = dict([line.strip().split('=', 1) for line in cookie.split(';')])
    return cookie

def extract_subset_of_dict(raw_dict, keys):
    subset = {}
    if isinstance(raw_dict, dict):
        subset = {key: value for key, value in raw_dict.items() if key in keys}
    return subset

def request(*args, **kwargs):
    is_retry = True
    count = 0
    max_retries = 3
    sleep_seconds = 5
    while is_retry and count <= max_retries:
        try:
            s = requests.Session()
            response = s.request(*args, **kwargs)
            is_retry = False
        except Exception as e:
            if count == max_retries:
                return False
            log.error(('Request failed: {}').format(e))
            count += 1
            log.info(
                ('Trying to reconnect in {} seconds ({}/{})...').format(
                    sleep_seconds, count, max_retries))
            time.sleep(sleep_seconds)
        else:
            return response