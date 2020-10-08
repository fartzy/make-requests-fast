import aiohttp
import asyncio
import itertools
import logging
import logging.handlers
from multipledispatch import dispatch
import os
import sys
import time
import urllib.request

from make_requests_fast.configuration import config
from make_requests_fast.utils.ListReader import ListReader
from make_requests_fast.requestors import Requestor


class AiohttpRequestor(Requestor):
    """
    Getting the requests using the asyncio event loop

    """

    def __init__(self, file):
        super(AiohttpRequestor, self).__init__(file)

        self.chunk_size = int(config.CHUNK_SIZE)

    @dispatch(object, object, int)
    async def load_url(self, session, url, timeout):
        self.log.info(f"Beginning request of {url}")
        async with session.get(url) as response:
            return (await response.text(), url)

    async def _execute(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                tasks.append(self.load_url(session, url, self.timeout_seconds))
            htmls = await asyncio.gather(*tasks)
            for html in htmls:
                self.log.info(f"The outcome of {html[1]} is {html[0]}\n")

    def execute(self):
        self.config_log()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._execute())


# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         file = sys.argv[1]
#     else:
#         file = "/Users/michaelartz/dev/python/make-requests-fast/make_requests_fast/resources/test_urls.csv"
#     aio = AiohttpRequestor(file)
#     aio.execute()