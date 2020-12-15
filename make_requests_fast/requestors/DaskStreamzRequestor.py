import concurrent.futures
import itertools
import multiprocessing
import sys
import time
import os
import urllib.request

from dask.distributed import Client
from streamz import Stream

from make_requests_fast.configuration import config
from make_requests_fast.utils.ListReader import ListReader
from make_requests_fast.requestors import Requestor


class DaskStreamzRequestor(Requestor):
    """
    Getting the requests with a DaskStreamzRequestor.

    """

    def __init__(self, file):
        super(DaskStreamzRequestor, self).__init__(file)
        self.max_workers = self._get_cpu_count()

    def _get_cpu_count(self):
        return multiprocessing.cpu_count()

    def get_client(self):
        client = Client()
        return client 

    def load_url_safe(self, url, timeout):
        ret_val = None
        try:
             return self.load_url(url, timeout)
        except self.client_exceptions as e:
             self.log_error(e, url)
             return (url, None)

    def log_info(self, result):
        url = result[0]
        if result[1]:
            html_size = sys.getsizeof(result[1])
            self.log.info(f"{url}, SUCCESS, {html_size}")
        else:
            self.log.info(f"{url}, FAIL, 0") 
        return

    def execute(self):
        self.config_log()
        client = self.get_client()

        #logger = Stream(asynchronous=True)

        stream = Stream()
        stream.map(self.load_url_safe, self.timeout_seconds) \
            .buffer(self._get_cpu_count() / 2) \
            .sink(self.log_info)

        for url in self.urls:
            stream.emit(url)

        client.close()

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         file = sys.argv[1]
#     else:
#         file = "/Users/mikeartz/dev/make-requests-fast/make_requests_fast/resources/test_urls.csv"
#     dsr = DaskStreamzRequestor(file)
#     dsr.execute()