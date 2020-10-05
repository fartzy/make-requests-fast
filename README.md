
# Make Requests Fast
  This is a project used to test diffferent libraries for parallelizing I/O tasks with python single node machine


### Requestors
Each Requestor uses a different way to parallelize http requests (excpet for ther sequential one which is not parallelized )
* SequentialRequestor
   - All requests are issued sequentially 
* ChunkedThreadPoolRequestor
   - Uses ThreadPoolExecutor from concurrent.futures
   - The futures are all returned when the whole chunk is done
   - A new chunk of futures is scheduled 
   - Since the GIL is released, this can improve upon sequential 
* BufferedChunkedThreadPoolRequestor
   - Uses ThreadPoolExecutor from concurrent.futures 
   - Each individual future is returned as soon as it is done
   - The program stays in a loop while and futures are not done
   - New future(s) are scheduled as they finish, up to the chunk size amount
   - Since the GIL is released, this can improve upon sequential 
* ChunkedProcessPoolRequestor
   - Uses ProcessPoolExecutor from concurrent.futures 
   - The futures are all returned when the whole chunk is done
   - A new chunk of futures is scheduled 
* MultiprocessThreadPoolRequestor
* AsyncioRequestor 


### Poetry usage 
This project uses Poetry.  Poetry is a tool that makes dependency managmeent cleaner and packaging easier.  
[Poetry documentation](https://python-poetry.org/docs/)
