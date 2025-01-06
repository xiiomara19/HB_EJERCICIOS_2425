import numpy as np
import math
import time as tm
import itertools
import random

# OBTENER INSTANCIA DE QAP
def read_instance(filepath):
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


# FUNCIÓN OBJETIVO DE QAP
def objective_function(solution, instance):
    size=instance[0]
    D=instance[1]
    H=instance[2]
    value=0

    for i in range(size):
        for j in range(size):
            value += D[i][j]*H[solution[i]][solution[j]]
 
    return value

# BRUTE FORCE
def lexicographic_next_permutation(a):
    i = len(a) - 2
    while not (i < 0 or a[i] < a[i+1]):
        i -= 1
    if i < 0:
        return False
    j = len(a) - 1
    while not (a[j] > a[i]):
        j -= 1
    a[i], a[j] = a[j], a[i]        
    a[i+1:] = reversed(a[i+1:])    
    return True

def brute_force(instance, permutation):
    best_sol = None
    best_value = float('inf')
    for _ in range(math.factorial(instance[0])):
        value = objective_function(permutation, instance)
        if value < best_value:
            best_value = value
            best_sol = permutation[:]
        lexicographic_next_permutation(permutation) 
    return (best_sol,best_value)

#RANDOM SEARCH
def random_search(instance, max_evaluations):
    size=instance[0]
    best_solution=np.random.permutation(size)
    best_value=objective_function(best_solution, instance)
    for _ in range(max_evaluations):
        candidate_solution=np.random.permutation(size)
        candidate_value=objective_function(candidate_solution, instance)
        if candidate_value<best_value:
            best_value=candidate_value
            best_solution=candidate_solution
    return (best_solution,best_value)


if __name__ == "__main__":
    print("¿Qué archivo quieres cargar?")
    archivo = int(input("1. tai5a.dat\n"
                        "2. tai10a.dat\n"
                        "3. tai20a.dat\n"))

    print("¿Qué caso de los siguientes probar?")
    algoritmo = int(input("1. Algoritmo Brute Force\n"
                          "2. Algoritmo Random Search con 100 evaluaciones\n"
                          "3. Algoritmo Random Search con 500 evaluaciones\n"
                          "4. Algoritmo Random Search con 1000 evaluaciones\n"))
    
    if archivo == 1:
        instance = read_instance("instances/tai5a.dat")
        print("Archivo tai5a.dat cargado \n")
    elif archivo == 2:
        instance = read_instance("instances/tai10a.dat")
        print("Archivo tai10a.dat cargado \n")
    elif archivo == 3:
        instance = read_instance("instances/tai20a.dat")
        print("Archivo tai20a.dat cargado \n")

    if algoritmo == 1:
        print("Algoritmo Brute Force\n")
        start = tm.time()
        permutation = list(next(itertools.permutations(range(instance[0]))))
        (bestFitness, bestSol) = brute_force(instance, permutation)
        end=tm.time()
    else:
        if algoritmo == 2:
            print("Algoritmo Random Search con 100 evaluaciones\n")
            max_evaluations = 100
        elif algoritmo == 3:
            print("Algoritmo Random Search con 500 evaluaciones\n")
            max_evaluations = 500
        elif algoritmo == 4:
            print("Algoritmo Random Search con 1000 evaluaciones\n")
            max_evaluations = 1000
        start = tm.time()
        (bestFitness,bestSol) = random_search(instance,max_evaluations)
        end=tm.time()
    
    print("Best fitness: {} Solution {}".format(bestFitness, bestSol))
    print("Execution time: {}".format(end-start))