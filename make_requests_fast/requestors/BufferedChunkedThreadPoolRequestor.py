import concurrent.futures
import itertools
import logging
import logging.handlers
from multipledispatch import dispatch
import sys
import time
import os
import urllib.request

from make_requests_fast.configuration import config
from make_requests_fast.utils.ListReader import ListReader
from make_requests_fast.requestors import Requestor


class BufferedChunkedThreadPoolRequestor(Requestor):
    """
    Getting the requests using the ThreadPoolExecutor and giving it chunks of size CHUNK_SIZE.
    And keeping the chunk full at all times.

    """

    def __init__(self, file):
        super(BufferedChunkedThreadPoolRequestor, self).__init__(file)

        self.chunk_size = int(config.CHUNK_SIZE)

    # Not needed, just changing the list to an iterator to save the state of the iteration
    # @dispatch(object, int, object)
    # def load_url(self, url, timeout, url_list):
    #     if url in url_list:
    #         url_list.remove(url)

    #     with urllib.request.urlopen(url, timeout=timeout) as conn:
    #         return conn.read()

    def execute(self):
        self.config_log()

        urls_left = iter(self.urls)

        with concurrent.futures.ThreadPoolExecutor() as executor:

            # Schedule the first N futures.  We don't want to schedule them all
            # at once, to avoid consuming excessive amounts of memory.
            futures = {
                executor.submit(self.load_url, url, self.timeout_seconds)
                for url in itertools.islice(urls_left, self.chunk_size)
            }

            while futures:
                # Wait for the next future to complete.
                done, futures = concurrent.futures.wait(
                    futures, return_when=concurrent.futures.FIRST_COMPLETED
                )

                for fut in done:
                    try:
                        html_size = sys.getsizeof(fut.result()[1])
                        self.log.info(f"{fut.result()[0]}, SUCCESS, {html_size}")
                    except self.client_exceptions as e:
                        self.log.error(e)

                # Schedule the next set of futures.  We don't want more than N futures
                # in the pool at a time, to keep memory consumption down.
                for url in itertools.islice(urls_left, len(done)):
                    futures.add(executor.submit(self.load_url, url, self.timeout_seconds))
