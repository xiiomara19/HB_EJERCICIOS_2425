import numpy as np
import time
import math
import itertools
import random
import statistics
import matplotlib.pyplot as plt


# QAParen instantzia diskotik irakurtzeko funtzioa
def read_instance_QAP(filepath):
    fp=open(filepath)
    line=fp.readline()
    values=line.split()
    size=int(values[0])
    D=np.zeros((size,size))
    H=np.zeros((size,size))
    for i in range(size):
        line=fp.readline()
        values=line.split()
        for j in range(size):
            D[i][j]=int(values[j])
        
    for i in range(size,2*size):
        line=fp.readline()
        values=line.split()
        for j in range(size):
            H[i-size][j]=int(values[j])
    fp.close()
    return (size,D,H)

# Soluzio bat emanik, bere helburu-funtzioaren balioa kalkulatuko duen funtzioa.
def objective_function_QAP(solution, instance):
    size=instance[0]
    D=instance[1]
    H=instance[2]
    value=0
    ## kalkulatu soluzio baten helburu funtzioaren balioa goiko ekuazioa ikusirik,
    # BETE HEMEN.
    for i in range(0,size):
        for j in range(0,size):
            value += D[i][j]*H[solution[i]][solution[j]]
    return value


def next_permutation(a):
    """Generate the lexicographically next permutation inplace.

    https://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order
    Return false if there is no next permutation.
    """
    # Find the largest index i such that a[i] < a[i + 1]. If no such
    # index exists, the permutation is the last permutation
    for i in reversed(range(len(a) - 1)):
        if a[i] < a[i + 1]:
            break  # found
    else:  # no break: not found
        return False  # no next permutation

    # Find the largest index j greater than i such that a[i] < a[j]
    j = next(j for j in reversed(range(i + 1, len(a))) if a[i] < a[j])

    # Swap the value of a[i] with that of a[j]
    a[i], a[j] = a[j], a[i]

    # Reverse sequence from a[i + 1] up to and including the final element a[n]
    a[i + 1:] = reversed(a[i + 1:])
    return True


#RANDOM SEARCH
def randomSearch(sol_ini, val_sol_ini, instance, size):
    respuestas=[]
    respuestas.append(val_sol_ini)
    pasos = 0
    t=10
    tiempoIni = time.time()
    optPer=sol_ini.copy()
    optVal=objective_function_QAP(optPer, instance)
    
    #while time.time() - tiempoIni < t:
    for j in range(0,361):
        pasos += 1
        comb2=np.random.permutation(size)
        res2=objective_function_QAP(comb2, instance)
        
        if res2<optVal:
            optPer=comb2.copy()
            optVal=res2
        respuestas.append(optVal)

    
    return respuestas, pasos



def generarVecino(V, i, j):
    #inserts hacia la derecha
    if i<=j:
        lag = V[i]
        for k in (range(i, j)):
            V[k] = V[k+1]
        V[j] = lag
        return list(V)
    #inserts hacia la izquierda
    else:
        lag = V[i]
        for k in reversed(range(j, i+1)):
            V[k] = V[k-1]
        V[j] = lag
        return list(V)

def generarTodosLosVecinos(sol_ini, size):
    vecinos = []
    
    for i in range(size):
        for j in range(i+1, size):
            aux = sol_ini.copy()
            vecino = generarVecino(aux, i, j)
            vecinos.append(vecino)
            
        for j in range(0, i-1):
            aux = sol_ini.copy()
            vecino = generarVecino(aux, i, j)
            vecinos.append(vecino)

            
    return vecinos

#BEST FIRST
def bestFirst(sol_ini, val_sol_ini, instance, size, vecindario):
    solucion = sol_ini.copy()
    pasos = 0
    
    respuestas=[]
    respuestas.append(val_sol_ini)
        
    for vecino in vecindario:
        pasos += 1
        val_vecino = objective_function_QAP(vecino, instance)
        if val_vecino <= val_sol_ini:
            respuestas.append(val_vecino)
            return respuestas, pasos
        
        else:
            respuestas.append(val_sol_ini)
    return respuestas, pasos

#GREEDY
def greedy(sol_ini, val_sol_ini, instance, size, vecindario):
    optimo = sol_ini.copy()
    valor_opt = val_sol_ini
    pasos = 0
    
    respuestas=[]
    respuestas.append(val_sol_ini)
        
    for vecino in vecindario:
        pasos += 1
        val_vecino = objective_function_QAP(vecino, instance)
        if val_vecino <= valor_opt:
            optimo = vecino.copy()
            valor_opt = val_vecino
        respuestas.append(valor_opt)

                
    return respuestas, pasos

def randomBL(sol_ini, val_sol_ini, instance, size, vecindario):
    optimo = sol_ini.copy()
    val_opt = val_sol_ini
    num_iter = 100
    pasos = 0
    
    respuestas=[]
    respuestas.append(val_sol_ini)
  
    
    vecinos = vecindario.copy()
    while vecinos:
        vecino = random.choice(vecinos)
        vecinos.remove(vecino)
        val_vecino = objective_function_QAP(vecino, instance)
        pasos += 1
        if val_vecino <= val_opt:
            val_opt =val_vecino
            optimo = vecino.copy()
        respuestas.append(val_opt)

            
    return respuestas, pasos
    
    
    
# tiempos1 = []
# steps1 = []
# resultados1 = []

# tiempos2 = []
# steps2 = []
# resultados2 = []

# tiempos3 = []
# steps3 = []
# resultados3 = []

# tiempos4 = []
# steps4 = []
# resultados4 = []

vecinos = []
instance=np.zeros(3)
instance=read_instance_QAP("/home/iraida/Desktop/4. maila/HB/tai20a.dat")
size=instance[0]

for i in range(1):
    solucion_inicial = np.random.permutation(size)
    
    valor_inicial = objective_function_QAP(solucion_inicial, instance)
    vecinos = generarTodosLosVecinos(solucion_inicial, size)


    # BEST FIRST
    # inicio = time.time()
    respuestasBF, pasos = bestFirst(solucion_inicial, valor_inicial, instance, size, vecinos)
    # fin = time.time()
    # tiempo = fin - inicio
    # tiempos1.append(tiempo)
    # resultados1.append(respuestasBF)
    # steps1.append(pasos)
    

    #---------------------------------------------------------
    # GREEDY
    
    # inicio = time.time()
    respuestasG, pasos = greedy(solucion_inicial, valor_inicial, instance, size, vecinos)
    # fin = time.time()
    # tiempo = fin - inicio
    # tiempos2.append(tiempo)
    # resultados2.append(respuestasG)
    # steps2.append(pasos)
    

    #---------------------------------------------------------
    # RANDOM BL
    
    # inicio = time.time()
    respuestasRBL, pasos = randomBL(solucion_inicial, valor_inicial, instance, size, vecinos)
    # fin = time.time()
    # tiempo = fin - inicio
    # tiempos3.append(tiempo)
    # resultados3.append(respuestasRBL)
    # steps3.append(pasos)
    

    
    #---------------------------------------------------------
    # RANDOM 
    
    # inicio = time.time()
    respuestasRS, pasos = randomSearch(solucion_inicial, valor_inicial, instance, size)
    # fin = time.time()
    # tiempo = fin - inicio
    # tiempos4.append(tiempo)
    # resultados4.append(respuestasRS)
    # steps4.append(pasos)
   
    
# media_pasos1 = statistics.mean(steps1)
# media_tiempos1 = statistics.mean(tiempos1)
# media_resultados1 = statistics.mean(resultados1)

# media_pasos2 = statistics.mean(steps2)
# media_tiempos2 = statistics.mean(tiempos2)
# media_resultados2 = statistics.mean(resultados2)

# media_pasos3 = statistics.mean(steps3)
# media_tiempos3 = statistics.mean(tiempos3)
# media_resultados3 = statistics.mean(resultados3)

# media_pasos4 = statistics.mean(steps4)
# media_tiempos4 = statistics.mean(tiempos4)
# media_resultados4 = statistics.mean(resultados4)
    
    
longitud_maxima = max(len(respuestasBF), len(respuestasG), len(respuestasRBL), len(respuestasRS))

# iteraciones = range(1,21)

steps = range(1, longitud_maxima+1)

respuestasBF += [None] * (longitud_maxima - len(respuestasBF))
respuestasG += [None] * (longitud_maxima - len(respuestasG))
respuestasRBL += [None] * (longitud_maxima - len(respuestasRBL))
respuestasRS += [None] * (longitud_maxima - len(respuestasRS))

plt.figure()
plt.plot(steps, respuestasBF, label="Best first", marker = "o")
plt.plot(steps, respuestasG, label="Greedy")
plt.plot(steps, respuestasRBL, label="Random (BL)")
plt.plot(steps, respuestasRS, label="Random search")

plt.xlabel("Número de Iteraciones")
plt.ylabel("Valores")
plt.legend()  # Mostrar la leyenda
plt.grid(True)  # Agregar una cuadrícula
plt.show()


