import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time
import os
import cProfile
from line_profiler import profile
from numba import njit, prange,set_num_threads


class JuegoDeLaVida:
    def __init__(self, rows=128, cols=128):  #aqui se puede cmabiar el tamaño de la grilla
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=bool)
        self.generation = 0

    def correrJuego(self):
        self.mostrarMenu()

#se muestra el menú de inicio con las opciones de juego.
    def mostrarMenu(self):
        opcion = None
        while opcion != "5":
            print("!JUEGO DE LA VIDA DE CONWAY!")
            print("1 - Crear tablero aleatorio")
            print("2 - cargar patrón desde archivo")
            print("3 - Ejecutar simulación")
            print("4 - Medir rendimiento/estadísticas")
            print("5 - Salir del juego")
            opcion = input("Indique su opción: ").strip()

            if opcion == "1":
                self.crearTableroAleatorio()
            elif opcion == "2":
                nombre = input("Nombre del patrón (sin escribir el '.txt)': ").strip()
                self.cargarPatronDesdeArchivo(nombre)
            elif opcion == "3":
                self.ejecutarSimulacion()
            elif opcion == "4":
                self.medirRendimiento()
            elif opcion == "5":
                print("Gracias por jugar.")
                break
            else:
                print("Opción no válida.")

    def crearTableroAleatorio(self): 
        print("Creando tablero aleatorio...")
        total_celdas = self.rows * self.cols
        cantidad = input(f"Ingrese la cantidad de células vivas (default 10, máximo {total_celdas}): ").strip()
        cantidad = int(cantidad) if cantidad else 10
        if cantidad < 1 or cantidad > total_celdas:
            print(f"La cantidad debe estar entre 1 y {total_celdas}.")
            return
        # Crear grilla vacía en caso de 'renniciar en le menú'
        self.grid = np.zeros((self.rows, self.cols), dtype=bool)
        indices = np.random.choice(total_celdas, size=cantidad, replace=False)
        for idx in indices:
            fila = idx // self.cols
            col = idx % self.cols
            self.grid[fila, col] = True
        self.generation = 0
        print(f"tablero creado con {cantidad} células vivas ({self.rows}x{self.cols})")

    def cargarPatronDesdeArchivo(self, nombre_archivo): #esta función agarra los patrones txt.
        if not nombre_archivo.endswith(".txt"):
            nombre_archivo += ".txt"
        if not os.path.exists(nombre_archivo):
            print(f"Archivo '{nombre_archivo}' no fue encontrado.")
            return
        try:
            self.grid = np.zeros((self.rows, self.cols), dtype=bool)
            with open(nombre_archivo, 'r') as f:
                lineas = f.readlines()
            patron = []
            for linea in lineas:
                fila = [int(i) for i in linea.strip() if i in "01"]
                if fila:
                    patron.append(fila)
            if not patron:
                print("El archivo está vacío o tiene formato inválido.")
                return
            patron = np.array(patron, dtype=bool)
            start_row = (self.rows - patron.shape[0]) // 2
            start_col = (self.cols - patron.shape[1]) // 2
            self.grid[start_row:start_row + patron.shape[0],
                      start_col:start_col + patron.shape[1]] = patron
            self.generation = 0
            print(f"Patrón cargado desde {nombre_archivo}")
        except Exception as e:
            print(f"Error al cargar el patrón: {e}")

    @profile
    def step(self): #este metodo es necesario para lograr que la configuración se ejecute en modo cuadricula de un kernel 3x3.
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])
        padded = np.pad(self.grid.astype(int), 1, mode='constant', constant_values=0)
        neighbor_count = sum(np.roll(np.roll(padded, i, 0), j, 1)[1:-1, 1:-1]
                             for i in (-1, 0, 1) for j in (-1, 0, 1) if (i != 0 or j != 0))

        #estas son las reglas en código
        new_grid = np.zeros_like(self.grid, dtype=bool)
        new_grid[self.grid & ((neighbor_count == 2) | (neighbor_count == 3))] = True
        new_grid[~self.grid & (neighbor_count == 3)] = True

        self.grid = new_grid
        self.generation += 1

    @profile
    def ejecutarSimulacion(self):
        if np.sum(self.grid) == 0:
            print("El tablero está vacío,cargue uno bien o cree uno aleatorio.")
            return
        try:
            generaciones = int(input("Cuántas generaciones quiere simular? (default 10): ") or 10)
            estado_inicial = self.grid.copy()
            generacion_inicial = self.generation

            for i in range(generaciones):
                self.step()
                if i % 10 == 0:
                    print(f"Generación {self.generation} / Células vivas: {np.sum(self.grid)}")
            self.mostrarResultado(estado_inicial, generacion_inicial)
        except ValueError:
            print("Valor inválido.")


    def mostrarResultado(self, estado_inicial, generacion_inicial):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7))
        colors = ['white', 'black']
        cmap = ListedColormap(colors)
        ax1.imshow(estado_inicial, cmap=cmap)
        ax1.set_title(f'Inicial (Gen {generacion_inicial})Vivas: {np.sum(estado_inicial)}')
        ax1.set_xticks([])
        ax1.set_yticks([])
        ax2.imshow(self.grid, cmap=cmap)
        ax2.set_title(f'Final (Gen {self.generation})Vivas: {np.sum(self.grid)}')
        ax2.set_xticks([])
        ax2.set_yticks([])
        plt.tight_layout()
        plt.show()

    def medirRendimiento(self):
        tamanios = [32, 64, 128, 256, 512]
        pasos = 10
        tiempos = []
        for tam in tamanios:
            self.rows, self.cols = tam, tam
            total_celdas = tam * tam
            cantidad = int(
                input(f"¿Cuántas células vivas desea para un tablero de {tam}x{tam} (max {total_celdas})?: "))
            cantidad = min(cantidad, total_celdas)
            self.grid = np.zeros((tam, tam), dtype=bool)
            indices = np.random.choice(total_celdas, size=cantidad, replace=False)
            for idx in indices:
                fila = idx // tam
                col = idx % tam
                self.grid[fila, col] = True
            self.generation = 0
            inicio = time.time()
            for _ in range(pasos):
                self.step()
            fin = time.time()
            tiempo_prom = (fin - inicio) / pasos
            tiempos.append(tiempo_prom)
            print(f"{tam}x{tam} - Tiempo promedio por paso: {tiempo_prom:.6f} segundos")
        plt.figure(figsize=(8, 6))
        plt.plot([tam * tam for tam in tamanios], tiempos, marker='o', label='Tiempos estimados')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Número de celdas (log scale)')
        plt.ylabel('Tiempo promedio por paso (segundos, log scale)')
        plt.title('Escalabilidad del juego.')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

#def main():
#    juego = JuegoDeLaVida()
#    juego.correrJuego()

# Parte 1,2,3 código para poner a prueba la simulación según el ejemplo dado.
import pstats

@njit(parallel=True)
def step_numba(grid):
    rows, cols = grid.shape
    new_grid = np.zeros((rows, cols), dtype=np.bool_)

    for i in prange(rows):
        for u in range(cols):
            vecinos_vivos = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, u + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if grid[ni, nj]:
                            vecinos_vivos += 1

            if grid[i,u]:
                new_grid[i,u] = vecinos_vivos == 2 or vecinos_vivos == 3
            else:
                new_grid[i,u] = vecinos_vivos == 3

    return new_grid

def simulacion_step(paralelo=True, hilos=1): #este valor es por defecto
    set_num_threads(hilos)
    grid = np.random.choice([True, False], size=(512, 512), p=[0.3, 0.7])
    #juego = JuegoDeLaVida(rows=512, cols=512)

    start = time.time()
    for i in range(100): # qui están los 100 pasos
        # juego.step()
         if paralelo:
             grid = step_numba(grid)
         else:
             pass
    end = time.time()
    print(f"{hilos} hilos, tiempo total: {end - start:.4f} segundos")
    return end - start


def prueba_escalamiento_con_grafico():
    tiempos = []
    hilos_usados = [1, 2, 4,6, 8,10,12]

    for h in hilos_usados:
        t = simulacion_step(paralelo=True, hilos=h)
        tiempos.append(t)

    speedup = [tiempos[0] / t for t in tiempos] #aquí se calculan el speedup y la eficiencia.
    eficiencia = [s / p for s, p in zip(speedup, hilos_usados)]

    plt.figure(figsize=(10, 6))
    plt.plot(hilos_usados, speedup, marker='o', label='Speedup')
    plt.plot(hilos_usados, eficiencia, marker='x', label='Eficiencia')
    plt.xlabel("Número de hilos (Numba)")
    plt.ylabel("Valor")
    plt.title("Escalamiento fuerte del Juego de la Vida")
    plt.grid(True)
    plt.legend()
    plt.xticks(hilos_usados)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    prueba_escalamiento_con_grafico()

