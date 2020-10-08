from datetime import datetime
import itertools
import logging
import logging.handlers
import os
import urllib.request

from make_requests_fast.utils.ListReader import ListReader
from make_requests_fast.configuration import config


class Requestor(object):
    def __init__(self, file):
        self.file = file
        self.urls = ListReader.read(self.file)
        self.timeout_seconds = int(config.TIMEOUT_SECONDS)
        self.log = logging.getLogger()

    def execute(self):
        """
        Execute the implementation of

        Args:
            start_date: Date for which to run the requestor.
        """
        pass

    def load_url(self, url, timeout):
        print(url)
        with urllib.request.urlopen(url, timeout=timeout) as conn:
            return (url, conn.read())

    def create_log_path(self, logging_dir=config.LOGGING_DIR):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"output_{date_time}.log"

        log_path = os.path.join(logging_dir, filename)
        self.log_path = log_path
        return log_path

    def config_log(self):

        handler = logging.handlers.WatchedFileHandler(
            os.environ.get("LOGFILE", self.create_log_path())
        )
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        handler.setFormatter(formatter)
        self.log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
        self.log.addHandler(handler)

    def chunked_iterable(self, iterable, size):
        it = iter(iterable)
        while True:
            chunk = tuple(itertools.islice(it, size))
            if not chunk:
                break
            yield chunk

    # TODO: Check details of the last run
    @staticmethod
    def get_last_run(table):
        pass