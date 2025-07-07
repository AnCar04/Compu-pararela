from numba import njit, prange, set_num_threads
import numpy as np
import matplotlib.pyplot as plt
import time
import os

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

def escalamiento_debil(pasos=100):
    hilos_lista = [1, 2, 4, 6, 8, 12]
    celdas_por_hilo = 100 * 100
    tiempos = []

    for h in hilos_lista:
        total_celdas = celdas_por_hilo * h
        tamanio = int(np.sqrt(total_celdas))

        set_num_threads(h)
        grid = np.random.choice([True, False], size=(tamanio, tamanio), p=[0.3, 0.7])
        inicio = time.time()
        for _ in range(pasos):
            grid = step_numba(grid)
        fin = time.time()
        duracion = fin - inicio
        tiempos.append(duracion)
        print(f"Hilos: {h}, Tamaño grilla: {tamanio}x{tamanio}, Tiempo total: {duracion:.4f} s")
    return hilos_lista, tiempos

def graficar_escalamiento_debil(hilos, tiempos):
    eficiencia = [tiempos[0] / t for t in tiempos]

    plt.figure(figsize=(10, 6))
    plt.plot(hilos, tiempos, marker='o', label='Tiempo total')
    plt.plot(hilos, eficiencia, marker='x', label='Eficiencia')
    plt.xlabel("Número de hilos")
    plt.ylabel("Tiempo / Eficiencia")
    plt.title("Escalamiento Débil juego de la Vida (Numba)")
    plt.grid(True)
    plt.legend()
    plt.xticks(hilos)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    hilos, tiempos = escalamiento_debil()
    graficar_escalamiento_debil(hilos, tiempos)