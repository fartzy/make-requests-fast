import concurrent.futures
import itertools
import sys
import time
import os
import urllib.request

from make_requests_fast.configuration import config
from make_requests_fast.utils.ListReader import ListReader
from make_requests_fast.requestors import Requestor


class ChunkedThreadPoolRequestor(Requestor):
    """
    Getting the requests using the ThreadPoolExecutor and giving it chunks of size CHUNK_SIZE.

    """

    def __init__(self, file):
        super(ChunkedThreadPoolRequestor, self).__init__(file)

        self.chunk_size = int(config.CHUNK_SIZE)

    def execute(self):
        self.config_log()

        for url_chunk in self.chunked_iterable(self.urls, self.chunk_size):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(self.load_url, task, self.timeout_seconds) for task in url_chunk
                }
                
                url = ""
                for fut in concurrent.futures.as_completed(futures):
                    try:
                        html_size = sys.getsizeof(fut.result()[1])
                        url = fut.result()[0] 
                        self.log.info(f"{url}, SUCCESS, {html_size}")
                    except self.client_exceptions as e:
                        self.log_error(e, url)
