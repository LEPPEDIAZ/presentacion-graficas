# -*- coding: cp1252 -*-
import simpy
import random

VELOCIDAD_PROCESADOR = 1
TIEMPO_WAITING = 1
CANTIDAD_PROCESADORES = 1
INSTRUCCIONES_POR_UNIDAD_DE_TIEMPO = 3
CANTIDAD_PROCESOS = 25
INTERVALO_GENERACION = 1
CANTIDAD_MEMORIA = 100

def generacionProcesos(env, cantidad, intervalo, procesador, memoriaDisponible):
    for i in range (cantidad):
        env.process(proceso("Proceso %d" % i, env, procesador, memoriaDisponible))
        t = random.expovariate(1.0 / intervalo)
        yield env.timeout(t)

def proceso(nombre, env, procesador, memoriaDisponible):
    instrucciones = random.randint(1,10)
    memoriaNecesaria = random.randint(1,10)
    instruccionesRestantes = instrucciones
    tiempoInicial = env.now

    #print('%s NEW' % nombre)
    while(memoriaDisponible.level<memoriaNecesaria):
        yield env.timeout(1)
    yield memoriaDisponible.get(memoriaNecesaria)
    #print('MEMORIA DISPONIBLE: %d | %s RESERVA: %d | MEMORIA RESTANTE: %d' % (memoriaDisponible.level+memoriaNecesaria, nombre, memoriaNecesaria, memoriaDisponible.level))

    while(instruccionesRestantes>0):
        #print ('%s READY' % nombre)
        with procesador.request() as procesar:
            yield procesar
            #print ('%s RUNNING' % nombre)
            yield env.timeout(VELOCIDAD_PROCESADOR)
            instruccionesRestantes -= INSTRUCCIONES_POR_UNIDAD_DE_TIEMPO
        if (instruccionesRestantes > 0):
            num = random.randint(1,2)
            if (num == 1):
                #print ('%s WAITING' % nombre)
                yield env.timeout(TIEMPO_WAITING)
    yield memoriaDisponible.put(memoriaNecesaria)
    global sumaTiempos
    sumaTiempos = sumaTiempos + env.now-tiempoInicial
    print ('%s TERMINATED | M: %s | I: %s | T: %s' % (nombre, str(memoriaNecesaria), str(instrucciones), str(env.now-tiempoInicial)))

sumaTiempos = 0
random.seed(10)
env = simpy.Environment()
procesador = simpy.Resource(env, capacity = CANTIDAD_PROCESADORES)
memoriaDisponible = simpy.Container(env, CANTIDAD_MEMORIA, init=CANTIDAD_MEMORIA)
env.process(generacionProcesos(env, CANTIDAD_PROCESOS, INTERVALO_GENERACION, procesador, memoriaDisponible))
env.run()

print ("SUMA DE TIEMPO: " + str(sumaTiempos))
tiempoPromedio = float(sumaTiempos)/float(CANTIDAD_PROCESOS)
print ("Tiempo promedio: " + str(tiempoPromedio))
