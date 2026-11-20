import threading
import time

T = 8
M = 200000

count = 0
sem = threading.Semaphore(1)


def tarefa():
    global count
    for i in range(M):
        sem.acquire()
        try:
            valor = count
            for j in range(10):
                pass
            count = valor + 1
        finally:
            sem.release()


lista = []
inicio = time.time()

for i in range(T):
    t = threading.Thread(target=tarefa)
    t.start()
    lista.append(t)

for t in lista:
    t.join()

fim = time.time()
print("esperado =", T * M, "obtido =", count, "tempo =", round(fim - inicio, 2), "segundos")
