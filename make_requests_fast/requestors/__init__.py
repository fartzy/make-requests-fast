from datetime import datetime
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
        with urllib.request.urlopen(url, timeout=timeout) as conn:
            return conn.read()

    def get_log_path(self):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"output_{date_time}.log"

        log_path = os.path.join(config.LOGGING_DIR, filename)
        return log_path

    def config_logger(self):

        handler = logging.handlers.WatchedFileHandler(
            os.environ.get("LOGFILE", self.get_log_path())
        )
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        handler.setFormatter(formatter)
        self.log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
        self.log.addHandler(handler)

    # TODO: Check details of the last run
    @staticmethod
    def get_last_run(table):
        pass