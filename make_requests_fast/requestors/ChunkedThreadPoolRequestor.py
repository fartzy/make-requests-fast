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

                for fut in concurrent.futures.as_completed(futures):
                    html_size = sys.getsizeof(fut.result()[1]) 
                    self.log.info(f"The outcome of {fut.result()[0]} is {html_size} bytes\n")
