from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# se valida que haya al menos 2 procesos
if size < 2:
    if rank == 0:
        print("Este programa requiere al menos 2 procesos.") #manejo de errores
    exit()

N = 10000
Tag = 1
mensaje = np.empty(1, dtype='b') #se crea el mensaje que es 1 byte.

#se hace la comunicación punto a punto
if rank == 0:
    comm.Barrier()  # sincronizar antes de medir
    start = time.perf_counter()
    
    for i in range(N):
        comm.Send([mensaje, MPI.BYTE], dest=1, tag=Tag)
        comm.Recv([mensaje, MPI.BYTE], source=1, tag=Tag)
    end = time.perf_counter()
    total_time = end - start
    latencia_promedio = (total_time / N) * 1_000_000
    print(f"Mensaje de 1 byte transmitido {N} veces.")
    print(f"Latencia promedio por mensaje (ida y vuelta): {latencia_promedio} microsegundos")
    print(f"Latencia estimada unidireccional: {latencia_promedio / 2} microsegundos")

elif rank == 1:
    comm.Barrier()  # sincronizar con el proceso 0
    for i in range(N):
        comm.Recv([mensaje,MPI.BYTE], source=0, tag=Tag)
        comm.Send([mensaje,MPI.BYTE], dest=0, tag=Tag) #aqu[i se realiza el ida y vuelta, ahora es del 1 al 0.
