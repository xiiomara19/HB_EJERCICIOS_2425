from operator import mod
import numpy as np
import random

"""XIOMARA GERALDINE CÁCERES CHANCAHUANA"""
"""HEURÍSTICOS DE BÚSQUEDA - 18/12/2024"""
dni=78956051
np.random.seed(dni)

#FUNCIONES OBJETIVO
#Distancia entre ciudades
def f1 (cities):
    distances = np.array([
        [0.0, 2009.98, 3354.1, 2000.0, 4136.66, 2061.55, 4427.19],
        [-1, 0.0, 3353.38, 3752.67, 2814.25, 3843.84, 4625.7],
        [-1, -1, 0.0, 1385.64, 2355.84, 2437.21, 1711.31],
        [-1, -1, -1, 0.0, 3348.58, 1140.18, 2159.62],
        [-1, -1, -1, -1, 0.0, 4262.32, 3590.83],
        [-1, -1, -1, -1, -1, 0.0, 3201.56]
    ])
    total_distance = 0
    num_cities = len(distances)

    for i in range(num_cities - 1):
        total_distance += distances[cities[3][i]][cities[3][i + 1]]
    
    return total_distance

#Coste de combustible
def f2 (cities):
    costs = np.array([
        [0.0, 1814.58, 3514.57, 2288.49, 4241.06, 2400.3, 4960.3],
        [-1, 0.0, 3674.66, 3873.63, 2612.13, 3846.72, 4644.27],
        [-1, -1, 0.0, 1524.62, 2212.34, 2642.68, 1936.63],
        [-1, -1, -1, 0.0, 3704.04, 1220.36, 2035.64],
        [-1, -1, -1, -1, 0.0, 4783.5, 3751.49],
        [-1, -1, -1, -1, -1, 0.0, 3272.27]
    ])
    total_distance = 0
    num_cities = len(costs)

    for i in range(num_cities - 1):
        total_distance += costs[cities[3][i]][cities[3][i + 1]]

    return total_distance

#Riesgo de robo
def f3 (cities):
    risks = np.array([
        [0.0, 0.4, 0.6, 0.7, 0.4, 0.6, 0.4],
        [-1, 0.0, 0.3, 0.5, 0.8, 0.7, 0.5],
        [-1, -1, 0.0, 0.1, 0.5, 0.6, 0.5],
        [-1, -1, -1, 0.0, 0.6, 0.7, 0.4],
        [-1, -1, -1, -1, 0.0, 0.9, 0.3],
        [-1, -1, -1, -1, -1, 0.0, 0.2],
    ])
    total_distance = 0
    num_cities = len(risks)

    for i in range(num_cities - 1):
        total_distance += risks[cities[3][i]][cities[3][i + 1]]

    return total_distance

#RESTRICCIONES
#Que se encuentre dentro de las coordenadas
def c1 (position):
    return 0<=position[0]<=5000 and 0<=position[1]<=5000

#Que haya recorrido las 7 ciudades
def c2 (cities):
    return len(cities) == 7

def inicializarModelo():

    return 0


"""
Estructura del ACO:
modelo = inicializarModelo() (feromonas)
while not condicion:
    solutions = nextSolution(modelo)

modelo = evaporar(modelo)
solution = actualizar(solution, modelo)
"""
def antColonyOptimization(colony_size, num_generations, alpha = 2, beta = 2, ro=2, Q=1):
    #1. Generar colonia inicial
    initialColony = []
    for _ in range(colony_size):
        x = np.random.uniform(0,5000)
        y = np.random.uniform(0,5000)
        cities = np.random.permutation(7).tolist()
        initialColony.append([x, y, cities])
    print("Colonia inicial: \n", initialColony)

    #2. Generar grafo ciudades
    cities = [
        ["Guru", 4500, 3000],       #Guru
        ["Porunga", 3200, 4700],    #Porunga
        ["Ajisa", 15000, 2000],     #Ajisa
        ["Moori", 2700, 1200],      #Moori
        ["Nameka", 400, 4000],      #Nameka
        ["Slug", 3800, 1000],       #Slug
        ["Dende", 800, 500]         #Dende
    ]

    #3. Inicializar modelo (feromonas)
    modelo = inicializarModelo()
    

    for i in range(num_generations):
        soluciones = []

        #Construir soluciones para cada hormiga


    return 0

#DOMINANCIA PARETO
def dominates(x, y):
    return np.all(x >= y) and np.any(x > y)

#FRONTERA-PARETO
def paretoFrontier (solution):
    pareto = []
    
    for i in range(len(solution)):
        isDominated = False
        for j in range(len(solution)):
            if i!=j and dominates(solution[j], solution[i]):
                isDominated = True
                break
        if not isDominated:
            pareto. append(solution[i])

    return np.array(pareto)


def getSolThreeObjFunctions(initialColony):
    objFunctionsSol = []
    for p in initialColony:
        s1 = f1(p[2])
        s2 = f2(p[2])
        s3 = f3(p[2])
        objFunctionsSol.append([s1, s2, s3])
    return objFunctionsSol

"""
Pasos a seguir del NSGA-2
1. Generar colonia inicial ´calculo de los valores
2. Realizar los pasos 3-5 la cantidad de num_generations
    2.3. Obtener siguiente generación con (not-sorted generation + coworking)
        a. De esa generación obtener los padres
        b. Crossover para obtener descendientes
        c. Mutar los descendientes
    2.4 Obtener generación nueva
    2.5. Unir y obtener las mejores hormigas k hormigas de la colonia
6. Obtener la mjor hormiga (el menor valor de las funciones objetivo)
"""
def nsga2(colony_size, num_generations):
    #1. Generar colonia inicial + calcular los valores
    initialColony = []
    for _ in range(colony_size):
        x = np.random.uniform(0,5000)
        y = np.random.uniform(0,5000)
        cities = np.random.permutation(7).tolist()
        initialColony.append([x, y, cities])
    print("Colonia inicial: \n", initialColony)

    objFunctionsSol = getSolThreeObjFunctions(initialColony)
    print("Soluciones funciones objetivo: \n", objFunctionsSol)

    for i in range(num_generations):
        i = 1


def main():
    result = mod(dni, 3)
    print ("Se va a probar la función objetivo", result+1, "para la segunda parte.")
    colony_size = 2
    num_generations = 10
    print("Ant Colony Optimization: \n")
    antColonyOptimization(colony_size, num_generations)

    print()
    print("")
    nsga2(colony_size, num_generations)

if __name__ == "__main__":
    main()