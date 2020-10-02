import time

import typer

from make_requests_fast.utils.ListReader import ListReader
from make_requests_fast.requestors.BufferedChunkedThreadPoolRequestor import (
    BufferedChunkedThreadPoolRequestor,
)
from make_requests_fast.requestors.MultiprocessThreadPoolRequestor import (
    MultiprocessThreadPoolRequestor,
)
from make_requests_fast.requestors.ChunkedProcessPoolRequestor import ChunkedProcessPoolRequestor
from make_requests_fast.requestors.ChunkedThreadPoolRequestor import ChunkedThreadPoolRequestor
from make_requests_fast.requestors.SequentialRequestor import SequentialRequestor

app = typer.Typer()


@app.command("run")
def run(
    requestor: str = typer.Option(
        "ChunkedThreadPool",
        "-r",
        "--requestor",
        help="type of requestor pool to use",
        show_default=True,
    ),
    file: str = typer.Option(
        "/Users/michaelartz/dev/python/make-requests-fast/make_requests_fast/resources/urls.csv",
        "-f",
        "--file",
        help="full path of file with urls",
        show_default=True,
    ),
):
    """Downloads the requests from a file in a location given

    We supply the type of pool concurrency and the full path of the file.
    """
    start_time = time.time()
    log_file = ""
    if requestor == "ChunkedThreadPool":
        ctpr = ChunkedThreadPoolRequestor(file)
        ctpr.execute()
        log_file = ctpr.log_path

    elif requestor == "Sequential":
        sr = SequentialRequestor(file)
        sr.execute()
        log_file = sr.log_path

    elif requestor == "BufferedChunkedThreadPool":
        bctpr = BufferedChunkedThreadPoolRequestor(file)
        bctpr.execute()
        log_file = bctpr.log_path

    elif requestor == "ChunkedProcessPool":
        cppr = ChunkedProcessPoolRequestor(file)
        cppr.execute()
        log_file = cppr.log_path

    elif requestor == "MultiprocessThreadPool":
        mtpr = MultiprocessThreadPoolRequestor(file)
        mtpr.execute()
        log_file = mtpr.log_path

    typer.echo(f"\nExecuted {requestor} with {file}")
    typer.echo(f"Log - {log_file}")
    typer.echo(f"---- %s seconds ----" % (time.time() - start_time))


def main():
    app()
