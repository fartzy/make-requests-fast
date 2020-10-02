from make_requests_fast import __version__
import multiprocessing as mp


def test_version():
    assert __version__ == "0.1.0"


def test_process_spawn():
    pass