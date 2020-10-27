import asyncio
import itertools
import logging
import logging.handlers
import os
import sys
import time
import urllib.request

import aiohttp
from multipledispatch import dispatch

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

        self.client_exceptions = (
            aiohttp.ClientResponseError,
            aiohttp.ClientConnectionError,
            aiohttp.ClientPayloadError,
            aiohttp.ServerDisconnectedError,
        )

    @dispatch(object, object, int)
    async def load_url(self, session, url, timeout):
        self.log.info(f"Beginning request of {url}")
        async with session.get(url) as response:
            return (await response.text(), url)

    # async def _shutdown(self, loop, signal=None):
    #     """Cleanup tasks tied to the service's shutdown."""
    #     if signal:
    #         self.log.info(f"Received exit signal {signal.name}...")
    #     self.log.info("Exiting Requestor")

    # def handle_exception(self, loop, context):
    #     # context["message"] will always be there; but context["exception"] may not
    #     msg = context.get("exception", context["message"])
    #     print(f"Caught exception: {msg}")
    #     print("Shutting down...")
    #     asyncio.create_task(self._shutdown(loop))    

    async def _execute(self):
        tasks = []
        try:
            async with aiohttp.ClientSession() as session:
                for url in self.urls:
                    tasks.append(self.load_url(session, url, self.timeout_seconds))
                htmls = await asyncio.gather(*tasks)
                for html in htmls:
                    self.log.info(f"The outcome of {html[1]} is {html[0]}\n")
        except self.client_exceptions as e:
            self.log.error(e)

    def execute(self):
        self.config_log()
        loop = asyncio.get_event_loop()
        # loop.set_exception_handler(self.handle_exception)
        loop.run_until_complete(self._execute())


# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         file = sys.argv[1]
#     else:
#         file = "/Users/michaelartz/dev/python/make-requests-fast/make_requests_fast/resources/test_urls.csv"
#     aio = AiohttpRequestor(file)
#     aio.execute()