from mpi4py import MPI
import numpy as np
#nota mpirun es el que ejcuta código en paralelo distribuido

#PARTE A
comm = MPI.COMM_WORLD #este es el comunicador general
rank = comm.Get_rank() #el id
size = comm.Get_size() #tamaño del comm

class EstadisticasMPI:
    def __init__(self, N=1000000): #aqui se puedr cambiar el tamaño de N
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        self.N = N

        if self.rank == 0:
            # Solo el proceso 0 define N
            if N is None:
                N = 1000000
            if N % self.size != 0:
                print(f"Error: N = {N} no es divisible entre {self.size}") #manejo de errores
                self.comm.Abort(1)
        else:
            N = None  # Los otros procesos no saben N aún

            #Aquí se usa Bcast para enviar N a todos los procesos
        self.N = self.comm.bcast(N, root=0)
        self.chunk_size = self.N // self.size
        self.subarreglo = np.empty(self.chunk_size, dtype=np.float64)

        if self.rank == 0:
            self.datos = np.random.uniform(0, 100, self.N)
        else:
            self.datos = None

    def distribuir_datos(self):
        self.comm.Scatter(self.datos, self.subarreglo, root=0)

    def calcular_estadisticas(self):
        local_min = np.min(self.subarreglo)
        local_max = np.max(self.subarreglo)
        local_sum = np.sum(self.subarreglo)

        global_min = self.comm.reduce(local_min, op=MPI.MIN, root=0)
        global_max = self.comm.reduce(local_max, op=MPI.MAX, root=0)
        global_sum = self.comm.reduce(local_sum, op=MPI.SUM, root=0)

        if self.rank == 0:
            global_avg = global_sum / self.N
            print(f"[Proceso 0] Estadísticas Globales:")
            print(f"mínimo: {global_min:.4f}")
            print(f"máximo: {global_max:.4f}")
            print(f"promedio: {global_avg:.4f}")

if __name__ == "__main__":
    app = EstadisticasMPI(N=1000000)
    app.distribuir_datos()
    app.calcular_estadisticas()

#PARTE B
