import concurrent.futures
import itertools
import sys
import time
import os
import urllib.request

from make_requests_fast.configuration import config
from make_requests_fast.utils.ListReader import ListReader
from make_requests_fast.requestors import Requestor


class SequentialRequestor(Requestor):
    """
    Getting the requests with a single thread.

    """

    def __init__(self, file):
        super(SequentialRequestor, self).__init__(file)

    def execute(self):
        self.config_log()

        for url in self.urls:
            html = self.load_url(url, self.timeout_seconds)
            html_size = sys.getsizeof(html[1])
            self.log.info(f"The outcome of {html[0]} is {html_size} bytes\n")