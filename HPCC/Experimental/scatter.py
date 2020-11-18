import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size() # new: gives number of ranks in comm
rank = comm.Get_rank()

numDataPerRank = 10
data = None
if rank == 0:
    data = [1,2,3,4,5,6]

recvbuf = [None] * 6 # allocate space for recvbuf
comm.Scatter(data, recvbuf, root=0)

print('Rank: ',rank, ', recvbuf received: ',recvbuf)