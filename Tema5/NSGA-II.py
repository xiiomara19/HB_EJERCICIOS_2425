import numpy as np
import math  # Import the math module
import random # Para crossover y mutación

#FUNCTIONS
def f1(x1, x2):
    return x1

def f2(x1, x2):
    return x2

#CONSTRAINTS
def C1(x1, x2):
    return x1**2 + x2**2 -1 -0.1*np.cos(16*np.arctan(x1/x2)) >= 0

def C2(x1, x2):
    return (x1-0.5)**2 + (x2-0.5)**2 <= 0.5

def C3(x1, x2):
    return 0 <= x1 <= np.pi and 0 <= x2 <= np.pi

def evaluateSolution (x1, x2):
    #Comprobar que cumple las restricciones
    if not (C1(x1, x2) and C2(x1, x2) and C3(x1, x2)):
        return [float('inf'), float('inf')] #INFEASIBLE SOLUTION
    return [f1(x1, x2), f2(x1, x2)] #FEASIBLE SOLUTION
                

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

#Divide las soluciones en niveles de frentes de pareto
def nonDominatedSorting (population):
    fronts = []                                 #Lista de fronteras pareto
    s = [[] for _ in range(len(population))]    #Lista de soluciones dominadas por la solución i
    n = np.zeros(len(population))               #Numero de soluciones que dominan a la solución i
    rank = np.zeros(len(population))            #Ranking de la solución i

    #Calcular dominancia
    for i,  p in enumerate(population):
        for j, q in enumerate(population):
            if dominates(p[2:], q[2:]):
                s[i].append(j)
            elif dominates(q[2:], p[2:]):
                n[i] += 1
        if n[i] == 0:
            rank[i] = 0
            if 0 not in fronts:
                fronts.append([])
            fronts[0].append(i)

    #Calcular fronteras
    k = 0
    while len(fronts[k]) > 0:
        next_front = []
        for i in fronts[k]:
            for j in s[i]:
                n[j] -= 1
                if n[j] == 0:
                    rank[j] = k+1
                    next_front.append(j)
        k += 1
        fronts.append(next_front)

    # Eliminar fronteras vacías
    fronts = [front for front in fronts if len(front) > 0]

    return fronts

#Mide la dispersion de las soluciones en el espacio de objetivos
def crowdingDistance (front, objective_functions):
    distances = np.zeros(len(front))
    num_objectives = len(objective_functions)
    for m in range(num_objectives):
        obj_values = [front[i][m] for i in range(len(front))]
        sorted_front = sorted(front, key=lambda x: x[m])
        distances[0] = float('inf')
        distances[-1] = float('inf')
        for i in range(1, len(front)-1):
            distances[i] += sorted_front[i+1][m] - sorted_front[i-1][m]

    return 0

def selectNextGeneration (population, objective_functions, pop_size):
    fronts = nonDominatedSorting(population)
    for i, f in enumerate(fronts):
        print("Front", i, ":", f)

    return population

def crossover (parent1, parent2):
    return [
        (parent1[0] + parent1[1]) / 2,
        (parent2[0] + parent2[1]) / 2
    ]

def mutation (offspring, mutation_rate=0.1):
    return [
        offspring[0] + mutation_rate * (random.random - 0.5),
        offspring[1] + mutation_rate * (random.random - 0.5)
    ]

def generateInitialValidPopulation (pop_size):
    population = []
    for _ in range(pop_size):
        x1 = np.random.uniform(0, np.pi)
        x2 = np.random.uniform(0, np.pi)
        [f1, f2] = evaluateSolution(x1, x2)
        if f1 != float('inf') and f2 != float('inf'):
            population.append([x1, x2, f1, f2])
    if len(population) < pop_size:
        pop = generateInitialValidPopulation(pop_size-len(population))
        for p in pop:
            population.append(p)
    return np.array(population)

#NSGA-II
def nsga2 (objective_functions, pop_size, num_generations):
    #1. Generar + evaluar población inicial (matriz)
    population = generateInitialValidPopulation(pop_size)
    #print(population)
    #print(len(population))

    #2. Repetir hasta max-iterations
    for generation in range(num_generations):

        #3. Frontera pareto
        pareto = paretoFrontier(population)
        #print(pareto)
        #print(len(pareto))

        #3. Seleccionar siguiente generación (non-dominated sorting + crowding distance)
        fronts = nonDominatedSorting(population)
        for i, f in enumerate(fronts):
            print("Front", i, ":", f)
        
        new_population = selectNextGeneration(population, objective_functions, pop_size)

        offsprings = []
        while len(offsprings) < pop_size:
            p1, p2 = random.sample(new_population, 2)
            #4. Cruzar
            [offspring1, offspring2] = crossover(p1, p2)
            #5. Mutar
            offspring = mutation([offspring1, offspring2])
            #6. Añadir a la población
            offsprings.append(offspring)

        #7.Mezclar y evaluar
        population = np.concatenate((population, offsprings), axis=0)
        

    return 0



objective_functions = [f1, f2]

final_population = nsga2(objective_functions, 100, 100)
