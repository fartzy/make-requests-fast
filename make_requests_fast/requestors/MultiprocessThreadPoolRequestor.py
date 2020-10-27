import concurrent.futures
import multiprocessing as mp
import itertools
import time
import os
import urllib.request

from make_requests_fast.configuration import config
from make_requests_fast.utils.ListReader import ListReader
from make_requests_fast.requestors import Requestor


class MultiprocessThreadPoolRequestor(Requestor):
    #TODO - Implement a a processpool which uses multiple threads for each process     
    """
    Getting the requests with a single thread.

    """

    def __init__(self, file):
        super(MultiprocessThreadPoolRequestor, self).__init__(file)

    def execute(self):
        self.config_log()

        for url in self.urls:
            html = self.load_url(url, self.timeout_seconds)
            self.log.info(f"The outcome of {html[0]} is {html[1]}\n")