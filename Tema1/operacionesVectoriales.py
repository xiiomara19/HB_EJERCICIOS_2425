import numpy as np
import time
import matplotlib.pyplot as plt
import tracemalloc

# Tamaño de la matriz cuadrada PROVISIONAL
n=100

# Generar número aleatorios reproducibles para la matriz
np.random.seed(1)

def multiplicacionMatrizVectorizada(A):
    matrix = np.dot(A,A)
    return matrix

def multiplicacionMatrizBucles(A):
    matrix = np.zeros((n,n))

    for  i in range(n):
        for j in range(n):
            for k in range(n):
                matrix[i,j] = matrix[i,j] + A[i,k]*A[k,j]
    return matrix

def generarGrafica(n, tiempos_bucles, tiempos_numpy, memorias_bucles, memorias_numpy):
    # Graficar
    plt.figure(figsize=(12, 6))

    # Tiempo de ejecución
    plt.subplot(1, 2, 1)
    plt.plot(n, tiempos_bucles, label="Bucles", marker="o")
    plt.plot(n, tiempos_numpy, label="Vectorizado", marker="o")
    plt.title("Tiempo de Ejecución")
    plt.xlabel("Tamaño de la Matriz ({t} x {t})".format(t=n))
    plt.ylabel("Tiempo (s)")
    plt.legend()

    # Uso de memoria
    plt.subplot(1, 2, 2)
    plt.plot(n, memorias_bucles, label="Bucles", marker="o")
    plt.plot(n, memorias_numpy, label="Vectorizado", marker="o")
    plt.title("Uso de Memoria")
    plt.xlabel("Tamaño de la Matriz ({t} x {t})".format(t=n))
    plt.ylabel("Memoria (KB)")
    plt.legend()

    plt.tight_layout()
    plt.savefig("comparacion_matrices.pdf")
    plt.show()
    


if __name__ == '__main__':
    # 1.Creación Matriz A
    print("####################### CREACIÓN MATRIZ A #######################")
    A = np.random.rand(n,n)
    print("Matriz A\n", A)

    # 2.Calculo de A**2 con funciones prexistentes
    print("\n####################### A**2 CON FUNCIONES PREXISTENTES #######################")
    time1 = time.time()
    tracemalloc.start()
    A21 = multiplicacionMatrizVectorizada(A)
    print("Matriz A**2 con funciones prexistentes\n", A21)
    usedMemory1, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    time2 = time.time()

    # 3.Calculo de A**2 con bucles (hard-coded)
    print("\n####################### A**2 CON BUCLES HARD-CODED #######################")
    time3 = time.time()
    tracemalloc.start()
    A22 = multiplicacionMatrizBucles(A)
    print("Matriz A**2 hard-coded\n", A22)
    usedMemory2, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    time4 = time.time()


    # 4. Comparación de tiempos
    print("\n####################### COMPARACIÓN DE TIEMPOS #######################")
    print("\nTiempo con funciones prexistentes: ", format(time2-time1))
    print("\nTiempo con bucles hard-coded: ", format(time4-time3))

    # 5. Comparación de memoria
    print("\n####################### COMPARACIÓN DE MEMORIA ########################")
    print("\nMemoria con funciones prexistentes: ", usedMemory1)
    print("\nMemoria con bucles hard-coded: ", usedMemory2)


    #6. Gráfica de eficiencia
    #print("####################### GRÁFICA DE EFICIENCIA ########################")
    generarGrafica([n], [time4-time3], [time2-time1], [usedMemory2], [usedMemory1])




