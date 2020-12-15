import concurrent.futures
import itertools
import multiprocessing
import sys
import time
import os
import urllib.request

from tenacity import retry, stop_after_attempt

from make_requests_fast.configuration import config
from make_requests_fast.utils.ListReader import ListReader
from make_requests_fast.requestors import Requestor


class ChunkedProcessPoolRequestor(Requestor):
    """
    Getting the requests with a ProcessPoolExecutor.

    """

    def __init__(self, file):
        super(ChunkedProcessPoolRequestor, self).__init__(file)
        self.max_workers = self._get_cpu_count()

    def _get_cpu_count(self):
        return multiprocessing.cpu_count()
            
    def execute(self):
        self.config_log()

        for url_chunk in self.chunked_iterable(self.urls, self.max_workers):
            with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self.load_url, url, self.timeout_seconds) for url in url_chunk
                }

                url = ""
                for fut in concurrent.futures.as_completed(futures):
                    try:
                        html_size = sys.getsizeof(fut.result()[1])
                        url = fut.result()[0] 
                        self.log.info(f"{url}, SUCCESS, {html_size}")
                    except self.client_exceptions as e:
                        self.log_error(e, url)
