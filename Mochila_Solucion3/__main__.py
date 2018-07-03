import sys
from random import randint
from random import random


def capturaDeDatos(): # Se capturan los datos importantes
    global numPoblacion, generaciones, probCruce, probMutacion, capacity, optimal_selection, profits, weights

    # Numero de individuos que tendra la poblacion
    numPoblacion = int(input("Ingrese el numero de la poblacion: "))
    while numPoblacion % 2 != 0 or numPoblacion < 2:
        print("Ingrese un numero de poblacion par\n")
        numPoblacion = int(input("Ingrese el numero de la poblacion: "))

    # Numero de genraciones (iteraciones)
    generaciones = int(input("Ingrese el numero de generaciones: "))
    while generaciones < 1:
        print("Ingrese un numero positivo mayor a 0\n")
        generaciones = int(input("Ingrese el numero de generaciones: "))

    # La probabilidad de cruce
    probCruce = float(input("Ingrese probabilidad de cruce (entre 0.65 y 0.80): "))
    while probCruce < 0.65 or probCruce > 0.80:
        print("Ingrese un valor entre 0.65 y 0.80\n")
        probCruce = float(input("Ingrese probabilidad de cruce (entre 0.65 y 0.80): "))

    # La probabilidad de mutacion
    probMutacion = float(input("Ingrese probabilidad de mutacion (entre 0.001 y 0.01): "))
    while probMutacion < 0.001 or probMutacion > 0.01:
        print("Ingrese un valor entre 0.001 y 0.01\n")
        probMutacion = float(input("Ingrese probabilidad de mutacion (entre 0.001 y 0.01): "))

    # Obtenemos la capacidad de la mochila
    with open('knapsack-capacity.txt', 'r') as file:
        capacity = int(file.read())

    # Llenamos los valores de ganancia
    with open('profits.txt', 'r') as file:
        for row in file:
            profits.append(row)

    # Lenamos los pesos de los objetos
    with open('weights.txt', 'r') as file:
        for row in file:
            weights.append(row)

    # Obtenemos el valor optimo
    with open('optimal-selection.txt', 'r') as file:
        for row in file:
            optimal_selection.append(row)


def inicializacion():  # Inicialiacion de la poblacion
    for i in range(0, numPoblacion):
        # Se genera el individuo para poder anexarlo al array individuos
        individuos.append(generarIndividuo())


def generarIndividuo():  # Genera la cadena binaria de los individuos
    individuo = ""
    for i in range(0, len(optimal_selection)):
        auxRandom = randint(0, 1)
        auxIndividuo = str(auxRandom)
        individuo = individuo + auxIndividuo
    return individuo


def seleccion():  # Seleccion de padres y generacion de valores para la tabla
    global auxF, sumX
    for i in range(0, numPoblacion):

        # Se convierte en decimal el valor binario
        x.append(obtenerPeso(i))

        # Se manda llamar al metodo de funcionObjetivo que devuelve el resultado esperado de fx
        fx.append(funcionObjetivo(i))

        # Se hace la sumatoria total de todos los valores de fx
        sumX = sumX + fx[i]

    # Se llena la tabla de fnorm con la operacion correspondiente
    for i in range(0, numPoblacion):
        fnorm.append(fx[i] / sumX)
        auxF = auxF + fnorm[i]

    # Si la norma de fnorm es igual a 1 sigue el procedimiento
    if 0.9 < auxF < 1.1:

        # Procedimiento para llenar la columna de acumulado
        for i in range(0, numPoblacion):
            if i == 0:
                acumulado.append(fnorm[i])
            else:
                acumulado.append(fnorm[i] + acumulado[i - 1])

            # Ademas se genera la tabla de numeros aleatorios para la seleccion de padres
            aleatorios.append(random())

        # Procedimiento para seleccionar los padres, por cada numero aleatorio se comparara con cada valor del acumulado
        for i in range(0, numPoblacion):
            for j in range(0, numPoblacion):

                # Si se cumple la condicion entonces se guarda la posicion del acumulado para detectar al padre
                if acumulado[j] > aleatorios[i]:
                    padresPosicion.append(j)
                    padres.append(individuos[j])
                    break

    # Si la norma de fnorm es diferente de 1 se acaba el programa
    else:
        solucion()
        sys.exit(0)


def funcionObjetivo(individuo): # Metodo que regresa el resultado de la funcion objetivo para guardarlo en el array fx
    ganancia = 0
    for i in range(0, len(optimal_selection)):
        ganancia += (int(individuos[individuo][i]) * int(profits[i]))
    return ganancia


def obtenerPeso(individuo):
    peso = 0
    for i in range(0, len(optimal_selection)):
        peso += (int(individuos[individuo][i]) * int(weights[i]))
    return peso


def cruce():  # Realiza el cruce genetico de los hijos
    global hijos
    hijos = padres
    for i in range(0, numPoblacion, 2):

        # Numero aleatorio de cruce
        auxAleatorio = random()

        # Se comprueba si se hace el cruce
        if auxAleatorio <= probCruce:

            # Generacion de puntos de corte
            puntoCorte1 = randint(0, 7)
            puntoCorte2 = randint(0, 7)
            while puntoCorte2 == puntoCorte1:
                puntoCorte2 = randint(0, 7)

            # Subcadena interna
            if puntoCorte1 < puntoCorte2:

                # Se generan las subcadenas para el intercambio
                cortePadre1 = padres[i][puntoCorte1:puntoCorte2+1]
                cortePadre2 = padres[i+1][puntoCorte1:puntoCorte2+1]

                # Se genera la cadena para los hijos con los cambios entre las cadenas
                hijos[i] = padres[i][:puntoCorte1] + cortePadre2 + padres[i][puntoCorte2 + 1:]
                hijos[i + 1] = padres[i + 1][:puntoCorte1] + cortePadre1 + padres[i + 1][puntoCorte2 + 1:]

            # Subcadenas externas
            elif puntoCorte1 > puntoCorte2:
                # Se generan las subcadenas para el intercambio
                padre1corte1 = padres[i][:puntoCorte2+1]
                padre1corte2 = padres[i][puntoCorte1:]
                padre2corte1 = padres[i + 1][:puntoCorte2 + 1]
                padre2corte2 = padres[i + 1][puntoCorte1:]

                # Se genera la cadena para los hijos con los cambios entre las cadenas
                hijos[i] = padre2corte1 + padres[i][puntoCorte2+1:puntoCorte1] + padre2corte2
                hijos[i + 1] = padre1corte1 + padres[i+1][puntoCorte2+1:puntoCorte1] + padre1corte2


def mutacion():
    global individuos, hijosAux, hijos, mejoresHijos

    # Se recorren todos los individuos
    for i in range(0, numPoblacion):

        # Se recorre cada cadena genetica del individuo
        for j in range(0, len(optimal_selection)):

            #Se genera el numero aleatorio
            auxAleatorio = random()

            # Si cumple la condicion hace el cambio de bit
            if auxAleatorio < probMutacion:
                if hijos[i][j] == "0":
                    hijos[i] = hijos[i][:j] + "1" + hijos[i][j + 1:]

                elif hijos[i][j] == "1":
                    hijos[i] = hijos[i][:j] + "0" + hijos[i][j + 1:]


    # Aqui se va a igualar los nuevos hijos a la poblacion de la nueva generacion, esto va al final de la mutacion
    individuos = hijos

    evaluacion()

    # Ordenamos de tal forma que se obtenga el mejor hijo y se lo agrgamos al array de mejoresHijos
    hijosAux = hijos.copy()

    obtenerMejorHijo(hijosAux)


def obtenerMejorHijo(listaux): # Obtiene el mejor hijo del arreglo dado
    global x, fx, mejorGanancia, mejorPeso, mejoresHijos
    x = []
    fx = []

    # Se llenasn las sdos listas para ver cual hijo es mejor en funcion de f(x)
    for i in range(0, len(listaux)):
        # Se obtiene el peso y ganancia
        ganancia = 0
        peso = 0
        for j in range(0, len(optimal_selection)):
            ganancia += (int(listaux[i][j]) * int(profits[j]))
            peso += (int(listaux[i][j]) * int(weights[j]))

        x.append(peso)
        fx.append(ganancia)

    for i in range(0,len(listaux)):
        if int(fx[i]) > int(mejorGanancia):
            mejoresHijos = listaux[i]
            mejorGanancia = fx[i]
            mejorPeso = x[i]


def solucion(): # Se muestra la solucion
    print("\nSeleccion optima:")
    print("\nCadena:", mejoresHijos, "\n")

    for i in range(0, len(optimal_selection)):
        if mejoresHijos[i] == '1':
            print("Objeto", i + 1, "\n Ganancia:", profits[i], "Peso:", weights[i])

    print("\nEl peso total es:", mejorPeso, "\nLa ganancia total es:", mejorGanancia)


def evaluacion():
    knapsack_overfield = False
    for i in range(0, numPoblacion):
        if obtenerPeso(i) > capacity:
            knapsack_overfield = True

        while (knapsack_overfield):
            j = randint(0, len(optimal_selection))
            individuos[i] = individuos[i][:j] + "0" + individuos[i][j+1:]
            if obtenerPeso(i) < capacity:
                knapsack_overfield = False



if __name__ == '__main__':
    # Inicializacion de Variables globales
    individuos = []
    x = []
    fx = []
    fnorm = []
    acumulado = []
    aleatorios = []
    padresPosicion = []
    padres = []
    mejoresHijos = "00000000"
    mejorGanancia = "0"
    mejorPeso = 0
    hijosAux = []

    capacity = 0
    optimal_selection = []
    profits = []
    weights = []

    # Funcion para pedir datos
    capturaDeDatos()

    # Se inicializa la primera generacion
    inicializacion()

    # Se evalua la poblacion
    evaluacion()

    # Ciclo para repetir las generaciones ingresadas
    for i in range(0, generaciones):
        # En cada generacion se resetean las sumatorias y los arreglos
        x = []
        fx = []
        fnorm = []
        acumulado = []
        aleatorios = []
        padresPosicion = []
        padres = []
        hijos = []

        auxF = 0.0
        sumX = 0.0

        # Empieza las operaciones del algoritmo genetico
        seleccion()
        cruce()
        mutacion()

    # Muestra la solucion
    solucion()

