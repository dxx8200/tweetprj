import wget
import os
import time
import socket

socket.setdefaulttimeout(300)

def bar_custom(current, total, width):
    pass

def download_file(src_url, dst_path, retry = 5, delay = 0.5):
    if src_url.rfind("?") >= 0:
        src_url = src_url[:src_url.rfind("?")]
    filename = src_url[src_url.rfind("/")+1:]
    filepath = os.path.join(dst_path, filename)
    if not os.path.exists(filepath):
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        i_retry = 0
        b_success = False
        while not b_success and i_retry < retry:
            try:
                wget.download(src_url, filepath, bar=bar_custom)
                b_success = True
                break
            except:
                time.sleep(0.5)
                i_retry += 1
        return b_success
    return True
