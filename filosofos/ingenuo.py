import threading
import time

garfos = [threading.Lock(), threading.Lock(), threading.Lock(), threading.Lock(), threading.Lock()]
vezes_que_comeu = [0, 0, 0, 0, 0]

def pensar(p):
    print(f"Filosofo {p} pensando")
    time.sleep(1)


def comer(p):
    print(f"Filosofo {p} comendo")
    vezes_que_comeu[p] += 1
    time.sleep(1)


def adquirir(p, garfo):
    garfos[garfo].acquire()
    print(f"Filosofo {p} pegou o garfo {garfo}")
    time.sleep(0.5)


def liberar(p, garfo):
    garfos[garfo].release()


def filosofo(p):
    left = p
    right = (p + 1) % 5
    while True:
        pensar(p)
        print(f"Filosofo {p} com fome")
        adquirir(p, left)
        adquirir(p, right)
        comer(p)
        liberar(p, right)
        liberar(p, left)


for p in range(5):
    threading.Thread(target=filosofo, args=(p,), daemon=True).start()

time.sleep(10)
print("FIM")
print("Vezes que cada um comeu:", vezes_que_comeu)