import time

import typer

from make_requests_fast.utils.ListReader import ListReader
from make_requests_fast.requestors.BufferedChunkedThreadPoolRequestor import (
    BufferedChunkedThreadPoolRequestor,
)

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

    if requestor == "ChunkedThreadPool":
        ChunkedThreadPoolRequestor(file).execute()
    elif requestor == "Sequential":
        SequentialRequestor(file).execute()
    elif requestor == "BufferedChunkedThreadPool":
        BufferedChunkedThreadPoolRequestor(file).execute()

    typer.echo(f"\nExecuted {requestor} with {file}")
    typer.echo(f"--- %s seconds ---" % (time.time() - start_time))


def main():
    app()
