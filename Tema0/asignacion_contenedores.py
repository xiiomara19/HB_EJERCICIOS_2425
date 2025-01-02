import numpy as np

# Define variables
k = 5
w = [77,72,89,30,29,19,34,68,35,44,55,92,93,78,14,36,95,56,87,18,63,51,85,37,37,1,89,16,43,44,35,16,6,12,56,92,51,64,49,93,22,77,4,74,64,40,9,73,77,9]
m = len(w)

print("# contenedores:",m)
print("Peso total:", sum(w))
print("# camiones:",k)
print("Estimación peso por camion:",sum(w)/k)

def suma (reparto, numCamion):
    suma = 0
    print('Camion:', numCamion)
    inicio = (numCamion-1)*m
    print("Inicio:", inicio)
    fin = numCamion*m
    print("Fin:", fin)
    
    for i in range(inicio, fin):
        if reparto[i] == 1:
            print("Posicion", i-m*(numCamion-1), "Valor", w[i-m*(numCamion-1)])
            suma += w[i-m*(numCamion-1)]
    return suma

def contenedoresNoRepetidos(reparto):
    for i in range(k):
        print(reparto[i-m*(numCamion-1)])
        if reparto[i-m*(numCamion-1)] == 1:
            return False
    return True

repartoFinal = np.zeros(m*k)
finished = False
numCamion = 1

while not finished:
    print("Camion:", numCamion)
    for i in range(len(repartoFinal)):
        if suma(repartoFinal, numCamion) < sum(w)/k and contenedoresNoRepetidos(repartoFinal):
            print("i", i)
            repartoFinal[i] = 1
            #print("Reparto:", repartoFinal)
        else:
            numCamion += 1

        if numCamion == k+1:
            finished = True
            break


print("Reparto final:", repartoFinal)
for i, value in enumerate(repartoFinal):
    print("Posición:", i, "con el valor", value)
