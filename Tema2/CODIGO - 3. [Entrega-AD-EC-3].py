from numpy import random
import numpy as np
import math

# ---------------------------------------- FUNCIÓN AUXILIAR - LEER FILE Y OBJECTIVE FUNCTION ----------------------------------------

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
    for i in range(size):
        for j in range(size):
            value += D[i][j] * H[solution[i]][solution[j]]
    return value

# ---------------------- EXCHANGE -------------------------
def ExchangeVector(V,i,j):
    lag = V[j]
    V[j]=V[i]
    V[i]=lag
    return V

def calcularVecinosExchange(N, vectorIni):
    vecinosExchange=[]
    vectorCopy = vectorIni.copy()
    # print("El vector inicial es así: vector  = ", vectorCopy)
    for i in range(0, N):
        for j in range(i+1, N):
            vector = vectorCopy.copy()
            # print("Esta iteración i=", i, ", j=", j)
            vectLag = ExchangeVector(vector,i,j)
            # print("VectLag = ", vectLag)
            vecinosExchange.append(vectLag)
    return vecinosExchange

# ---------------------- ALGORITMO BEST FIRST -------------------------
def calcularMejorVecinosExchangeBestFirst(instance, N, vectorIni, valorIni):
    vectorCopy = vectorIni.copy()

    optimo_global_encontrado = False
    valor_solucion_local = valorIni
    solucion_local= vectorIni

    #print("El vector inicial es así: vector  = ", vectorCopy)
    for i in range(0, N):
        for j in range(i+1, N):
            vector = vectorCopy.copy()
            # print("Esta iteración i=", i, ", j=", j)
            vectLag = ExchangeVector(vector,i,j)
            valor_solucion_vecina = objective_function_QAP(vectLag, instance)
            # print("COMO VECINO DE ", vectorCopy, "SE HA SACADO EL VECINO: ", vectLag, ", VALOR ", valor_solucion_vecina)
            if valor_solucion_local > valor_solucion_vecina:
                valor_solucion_local = valor_solucion_vecina
                solucion_local = vectLag
                return (optimo_global_encontrado, valor_solucion_local, solucion_local)

    if valorIni == valor_solucion_local: 
        optimo_global_encontrado = True

    return (optimo_global_encontrado, valor_solucion_local, solucion_local)

def best_first_solution(possible_solution, size, i_max, instance):
    i = 0
    optimo_global_encontrado = False

    solucion_global = possible_solution
    valor_solucion_global = objective_function_QAP(solucion_global, instance)

    solucion_local = None
    valor_solucion_local = None

    while i<i_max and not optimo_global_encontrado:
        # print("\n BEST FIRST SOLUTION interation number = ", i)
        # print("NODO ACTUAL --> SOLUCIÓN = ", solucion_global, ", VALOR = ", valor_solucion_global)
        (optimo_global_encontrado, valor_solucion_local, solucion_local) = calcularMejorVecinosExchangeBestFirst(instance, size, solucion_global, valor_solucion_global )
        # print("LO QUE HA DEVUELTO calcularMejorVecinosExchangeBestFirst: ")
        # print("      optimo_global_encontrado = ", optimo_global_encontrado)
        # print("      valor_solucion_local = ", valor_solucion_local)
        # print("      solucion_local = ", solucion_local)
        if valor_solucion_local < valor_solucion_global:
            valor_solucion_global = valor_solucion_local
            solucion_global= solucion_local
        i = i + 1
    return (optimo_global_encontrado, valor_solucion_global, solucion_global)

# ---------------------- ALGORITMO GREEDY -------------------------
def calcularMejorVecinosExchangeGreedy(instance, N, vectorIni, valorIni):
    vectorCopy = vectorIni.copy()

    optimo_global_encontrado = False
    valor_solucion_local = valorIni
    solucion_local= vectorIni

    #print("El vector inicial es así: vector  = ", vectorCopy)
    for i in range(0, N):
        for j in range(i+1, N):
            vector = vectorCopy.copy()
            # print("Esta iteración i=", i, ", j=", j)
            vectLag = ExchangeVector(vector, math.floor(random.uniform(i,j)), math.floor(random.uniform(i,j)))
            valor_solucion_vecina = objective_function_QAP(vectLag, instance)
            # print("COMO VECINO DE ", vectorCopy, "SE HA SACADO EL VECINO: ", vectLag, ", VALOR ", valor_solucion_vecina)
            if valor_solucion_local > valor_solucion_vecina:
                valor_solucion_local = valor_solucion_vecina
                solucion_local = vectLag

    if valorIni == valor_solucion_local: 
        optimo_global_encontrado = True

    return (optimo_global_encontrado, valor_solucion_local, solucion_local)

def greedy_search_solution(possible_solution, size, i_max, instance):
    i = 0
    optimo_global_encontrado = False

    solucion_global = possible_solution
    valor_solucion_global = objective_function_QAP(solucion_global, instance)

    solucion_local = None
    valor_solucion_local = None

    while i<i_max and not optimo_global_encontrado:
        # print("\n BEST FIRST SOLUTION interation number = ", i)
        # print("NODO ACTUAL --> SOLUCIÓN = ", solucion_global, ", VALOR = ", valor_solucion_global)
        (optimo_global_encontrado, valor_solucion_local, solucion_local) = calcularMejorVecinosExchangeGreedy(instance, size, solucion_global, valor_solucion_global )
        # print("LO QUE HA DEVUELTO calcularMejorVecinosExchangeBestFirst: ")
        # print("      optimo_global_encontrado = ", optimo_global_encontrado)
        # print("      valor_solucion_local = ", valor_solucion_local)
        # print("      solucion_local = ", solucion_local)
        if valor_solucion_local < valor_solucion_global:
            valor_solucion_global = valor_solucion_local
            solucion_global= solucion_local
        i = i + 1
    return (optimo_global_encontrado, valor_solucion_global, solucion_global)


# ---------------------------------------- ----------------------- ----------------------------------------
# ---------------------------------------- EJECUTAR DESDE EL MAIN  ----------------------------------------
# ---------------------------------------- ----------------------- ----------------------------------------

# ---------------------------------------- TECNICAS BÚSQUEDA DE ÓPTIMOS LOCALES ----------------------------------------

def ejecutar_best_fist(i_max, instance, size):
    possible_solution = np.random.permutation(size)  # Solución inicial aleatoria
    (optimo_global_encontrado, valor_solucion_global, solucion_global) = best_first_solution(possible_solution, size, i_max, instance)
    print("Máximas iteraciones =  ", i_max)
    print("Se ha encontrado un óptimo local? ", optimo_global_encontrado)
    print("Solución sub-óptima = ", solucion_global)
    print("Valor de la solución sub-óptima = ", valor_solucion_global, "\n")

def ejecutar_greedy(i_max, instance, size):
    possible_solution = np.random.permutation(size)  # Solución inicial aleatoria
    (optimo_global_encontrado, valor_solucion_global, solucion_global) = greedy_search_solution(possible_solution, size, i_max, instance)
    print("Máximas iteraciones =  ", i_max)
    print("Se ha encontrado un óptimo local? ", optimo_global_encontrado)
    print("Solución sub-óptima = ", solucion_global)
    print("Valor de la solución sub-óptima = ", valor_solucion_global, "\n")


# ---------------------------------------- TECNICAS PARA LA ESTIMACIÓN DE ÓPTIMOS LOCALES ----------------------------------------

def ejecutar_Chao_1984_Chao_and_Lee_1992_Chao_and_Bunge_2002(i_max, m, instance, size):
    r_soluciones = []
    for i in range(m):
        possible_solution = np.random.permutation(size)
        (optimo_global_encontrado, valor_solucion_global, solucion_global) = best_first_solution(possible_solution, size, i_max, instance)
        
        # Verificar si la solución ya está en r_soluciones usando np.array_equal
        if not any(np.array_equal(solucion_global, existing_solution) for existing_solution in r_soluciones):
            r_soluciones.append(solucion_global)

    r = len(r_soluciones)
    indice = r/m

    print("1.- Elegir m soluciones al azar, m =",m)
    print("2.- Aplicar Best First sobre las soluciones")
    print("3.- Contar los óptimos locales r, r = ", r)
    print("4.- Calcular el índice r / m = ", indice)



def ejecutar_schnabel_census_procedure(i_max, m, instance, size):
    r = 0
    for i in range(m):
        possible_solution = np.random.permutation(size)
        (optimo_global_encontrado, valor_solucion_global, solucion_global) = greedy_search_solution(possible_solution, size, i_max, instance)
        if optimo_global_encontrado:
            r+=1
    indice = r/m

    print("1.- Elegir m soluciones al azar, m =",m)
    print("2.- Aplicar greedy sobre las soluciones")
    print("3.- Contar los óptimos locales r, r = ", r)
    print("4.- Calcular el índice r / m = ", indice)


# ---------------------------------------- ---- ----------------------------------------
# ---------------------------------------- MAIN ----------------------------------------
# ---------------------------------------- ---- ----------------------------------------

path1 = "tai5a.dat"
path2 = "tai10a.dat"
path3 = "tai20a.dat"
i_max = 1000
m = random.randint(100)




print(" \n ---------------------------------------- --------------------------------------------- ----------------------------------------")
print(" ---------------------------------------- TECNICAS DE BÚSQUEDA LOCAL ---------------------------------------- ")
print(" ---------------------------------------- --------------------------------------------- ---------------------------------------- \n ")



# ---------------------------------------- RESULTADOS BEST FIRST ----------------------------------------
print(" \n ------- ESTOS SON LOS RESTULTADOS DE BUSQUEDA LOCAL CON BEST FIRST -------\n ")

#---------------------------------------- tai5a.dat 
print(" \n ---- SOLUCIONES tai5a.dat ----")
instance = read_instance_QAP(path1)
size = instance[0]
ejecutar_best_fist(i_max, instance, size)


#---------------------------------------- tai10a.dat 
print(" \n ---- SOLUCIONES tai10a.dat ----")
instance = read_instance_QAP(path2)
size = instance[0]
ejecutar_best_fist(i_max, instance, size)


#---------------------------------------- tai20a.dat 
print(" \n ---- SOLUCIONES tai20a.dat ----")
instance = read_instance_QAP(path3)
size = instance[0]
ejecutar_best_fist(i_max, instance, size)


# ---------------------------------------- RESULTADOS GREEDY ----------------------------------------
print(" ------- ESTOS SON LOS RESTULTADOS DE BUSQUEDA LOCAL CON GREEDY -------")

#---------------------------------------- tai5a.dat 
print(" \n ---- SOLUCIONES tai5a.dat ----")
instance = read_instance_QAP(path1)
size = instance[0]
ejecutar_greedy(i_max, instance, size)



#---------------------------------------- tai10a.dat 
print(" \n ---- SOLUCIONES tai10a.dat ----")
instance = read_instance_QAP(path2)
size = instance[0]
ejecutar_greedy(i_max, instance, size)



#---------------------------------------- tai20a.dat 
print(" \n ---- SOLUCIONES tai20a.dat ----")
instance = read_instance_QAP(path3)
size = instance[0]
ejecutar_greedy(i_max, instance, size)



print(" \n ---------------------------------------- --------------------------------------------- ----------------------------------------")
print(" ---------------------------------------- TECNICAS PARA LA ESTIMACIÓN DE ÓPTIMOS LOCALES ---------------------------------------- ")
print(" ---------------------------------------- --------------------------------------------- ---------------------------------------- \n ")
i_max = 100



print(" \n -------------------- Chao 1984, Chao & Lee 1992, Chao & Bunge 2002 -------------------- ")

#---------------------------------------- tai5a.dat 
# La m ideal sería 5! (120) para que puediese llegar a todas las combinaciones posibles de permutaciones
print(" \n ---- SOLUCIONES tai5a.dat ----")
instance = read_instance_QAP(path1)
size = instance[0]
ejecutar_Chao_1984_Chao_and_Lee_1992_Chao_and_Bunge_2002(i_max, m, instance, size)

#---------------------------------------- tai10a.dat 
# La m ideal sería 10! (3628800) para que puediese llegar a todas las combinaciones posibles de permutaciones
print(" \n ---- SOLUCIONES tai10a.dat ----")
instance = read_instance_QAP(path2)
size = instance[0]
ejecutar_Chao_1984_Chao_and_Lee_1992_Chao_and_Bunge_2002(i_max, m, instance, size)

#---------------------------------------- tai20a.dat 
# La m ideal sería 20! (2432902008176640000) para que puediese llegar a todas las combinaciones posibles de permutaciones
print(" \n ---- SOLUCIONES tai20a.dat ----")
instance = read_instance_QAP(path3)
size = instance[0]
ejecutar_Chao_1984_Chao_and_Lee_1992_Chao_and_Bunge_2002(i_max, m, instance, size)


print(" \n -------------------- Schnabel Census Procedure -------------------- ")

#---------------------------------------- tai5a.dat 
# La m ideal sería 5! (120) para que puediese llegar a todas las combinaciones posibles de permutaciones
print(" \n ---- SOLUCIONES tai5a.dat ----")
instance = read_instance_QAP(path1)
size = instance[0]
ejecutar_schnabel_census_procedure(i_max, m, instance, size)


#---------------------------------------- tai10a.dat 
# La m ideal sería 10! (3628800) para que puediese llegar a todas las combinaciones posibles de permutaciones
print(" \n ---- SOLUCIONES tai10a.dat ----")
instance = read_instance_QAP(path2)
size = instance[0]
ejecutar_schnabel_census_procedure(i_max, m, instance, size)

#---------------------------------------- tai20a.dat 
# La m ideal sería 20! (2432902008176640000) para que puediese llegar a todas las combinaciones posibles de permutaciones
print(" \n ---- SOLUCIONES tai20a.dat ----")
instance = read_instance_QAP(path3)
size = instance[0]
ejecutar_schnabel_census_procedure(i_max, m, instance, size)