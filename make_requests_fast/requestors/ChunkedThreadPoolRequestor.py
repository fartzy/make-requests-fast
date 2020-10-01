import concurrent.futures
import itertools
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

    def _chunked_iterable(self, iterable, size):
        it = iter(iterable)
        while True:
            chunk = tuple(itertools.islice(it, size))
            if not chunk:
                break
            yield chunk

    def execute(self):
        self.config_logger()

        for task_set in self._chunked_iterable(self.urls, self.chunk_size):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(self.load_url, task, self.timeout_seconds) for task in task_set
                }

                for fut in concurrent.futures.as_completed(futures):
                    self.log.info(f"The outcome is {fut.result()}\n")


# if __name__ == "__main__":
#     start_time = time.time()
#     execute()
#     print("--- %s seconds ---" % (time.time() - start_time))
