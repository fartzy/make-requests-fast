import os
import time

import typer

from make_requests_fast.utils.ListReader import ListReader
from make_requests_fast.requestors.AiohttpRequestor import AiohttpRequestor
from make_requests_fast.requestors.DaskStreamzRequestor import DaskStreamzRequestor
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
        "all",
        "-r",
        "--requestor",
        help="type of requestor pool to use",
        show_default=True,
    ),
    file: str = typer.Option(
        f"{os.getcwd()}/make_requests_fast/resources/urls.csv",
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
        print_out("ChunkedThreadPool", file, ctpr.log_path, start_time)

    elif requestor == "Sequential":
        sr = SequentialRequestor(file)
        sr.execute()
        print_out("Sequential", file, sr.log_path, start_time)

    elif requestor == "BufferedChunkedThreadPool":
        bctpr = BufferedChunkedThreadPoolRequestor(file)
        bctpr.execute()
        print_out("BufferedChunkedThreadPool", file, bctpr.log_path, start_time)

    elif requestor == "ChunkedProcessPool":
        cppr = ChunkedProcessPoolRequestor(file)
        cppr.execute()
        print_out("ChunkedProcessPool", file, cppr.log_path, start_time)

    # TODO: Implement MultiprocessThreadPoolRequestor
    # elif requestor == "MultiprocessThreadPool":
    #     mtpr = MultiprocessThreadPoolRequestor(file)
    #     mtpr.execute()
    #     print_out("MultiprocessThreadPool", file, mtpr.log_path, start_time)

    elif requestor == "Aiohttp":
        aioh = AiohttpRequestor(file)
        aioh.execute()
        print_out("Aiohttp", file, aioh.log_path, start_time)


    elif requestor == "all":
        start_time = time.time()
        aioh = AiohttpRequestor(file)
        aioh.execute()
        print_out("Aiohttp", file, aioh.log_path, start_time)

        start_time = time.time()
        bctpr = BufferedChunkedThreadPoolRequestor(file)
        bctpr.execute()
        print_out("BufferedChunkedThreadPool", file, bctpr.log_path, start_time)

        start_time = time.time()
        dsr = DaskStreamzRequestor(file)
        dsr.execute()
        print_out("DaskStreamz", file, dsr.log_path, start_time)

        start_time = time.time()
        cppr = ChunkedProcessPoolRequestor(file)
        cppr.execute()
        print_out("ChunkedProcessPool", file, cppr.log_path, start_time)

        # TODO: Implement MultiprocessThreadPoolRequestor
        # start_time = time.time()
        # mtpr = MultiprocessThreadPoolRequestor(file)
        # mtpr.execute()
        # print_out("MultiprocessThreadPool", file, mtpr.log_path, start_time)

        start_time = time.time()
        ctpr = ChunkedThreadPoolRequestor(file)
        ctpr.execute()
        print_out("ChunkedThreadPool", file, ctpr.log_path, start_time)

        start_time = time.time()
        sr = SequentialRequestor(file)
        sr.execute()
        print_out("Sequential", file, sr.log_path, start_time)


def print_out(requestor, file, log_file, start_time):
    typer.echo(f"\nExecuted {requestor} with {file}")
    typer.echo(f"Log - {log_file}")
    typer.echo(f"---- %s seconds ----" % (round((time.time() - start_time), 3)))

def main():
    app()
