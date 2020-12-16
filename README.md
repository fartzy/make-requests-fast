
# Make Requests Fast
  This is a project used to test different libraries for parallelizing I/O tasks with python single node machine


## Install Poetry
This project uses Poetry version 1.1.0rc1.  The latest at this time is 1.1.3 so just use that.
   > pip install --user poetry
   > poetry self update 1.1.3

Poetry is a tool that makes dependency managmeent cleaner and packaging easier.  [Poetry documentation](https://python-poetry.org/docs/)


## Install project
Download the code from Github and then use poetry to install the dependencies on your machine
   > git clone https://github.com/fartzy/make-requests-fast.git

Create a new python environment with Poetry for this project 
   > poetry env use 3.8

Install the dependencies for this project using Poetry 
   > poetry install 

Start the poetry shell 
   > poetry shell 

## Run 
* This project uses the typer module. To execute a type of Requestor, give the name of the file and the type of requestor, without "Requestor". Only the abosulte path has been tested. 
* Examples: 
    >  mrf -r ChunkedLoopedThreadPool -f /path/to/make-requests-fast/make_requests_fast/resources/urls.csv   
    >
    >  mrf -r BufferedChunkedThreadPool -f /path/to/make-requests-fast/make_requests_fast/resources/urls.csv 
    >
    >  mrf -r Sequential -f /path/to/make-requests-fast/make_requests_fast/resources/urls.csv 
    > 
    >  mrf -r ChunkedProcessPool -f /path/to/make-requests-fast/make_requests_fast/resources/urls.csv 
    > 
    >  mrf -r Aiohttp -f /path/to/make-requests-fast/make_requests_fast/resources/urls.csv 


### Requestors
Each Requestor uses a different way to parallelize http requests ( except for SequentialRequestor one which does not parallelize )
* SequentialRequestor
   * All requests are issued sequentially 
* ChunkedThreadPoolRequestor
   * Uses ThreadPoolExecutor from concurrent.futures
   * The futures are all returned when the whole chunk is done
   * A new chunk of futures is scheduled 
   * Since the GIL is released, this can improve upon sequential 
* BufferedChunkedThreadPoolRequestor
   * Uses ThreadPoolExecutor from concurrent.futures 
   * Each individual future is returned as soon as it is done
   * The program stays in a loop while and futures are not done
   * New future(s) are scheduled as they finish, up to the chunk size amount
   * Since the GIL is released, this can improve upon sequential
* ChunkedProcessPoolRequestor
   * Uses ProcessPoolExecutor from concurrent.futures 
   * The futures are all returned when the whole chunk is done
   * A new chunk of futures is scheduled 
* AiohttpRequestor 
   * Uses aiohttp which uses asycnio 
   * Not currently using the speedup libraries (Will add them in future)
      - cchardet, aiodns, brotlipy
   * Creates and event loop and adds tasks to the event loop 
   * Each task is a coroutine which executes an individual http request
* DaskStreamzRequestor
   * Uses streamz reactive API 
   * `scatter()` causes the stream to be distributed to dask cluster 
   * buffer ( the amount of partitions ) is set at total number of cores / 2
   * the dask cluster is local only 



