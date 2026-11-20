import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()


def thread1():
    print("T1 esperando LOCK_A")
    LOCK_A.acquire()
    print("T1 pegou LOCK_A")
    time.sleep(0.05)
    print("T1 esperando LOCK_B")
    LOCK_B.acquire()
    print("T1 pegou LOCK_B")
    print("T1 concluiu")
    LOCK_B.release()
    LOCK_A.release()


def thread2():
    print("T2 esperando LOCK_B")
    LOCK_B.acquire()
    print("T2 pegou LOCK_B")
    time.sleep(0.05)
    print("T2 esperando LOCK_A")
    LOCK_A.acquire()
    print("T2 pegou LOCK_A")
    print("T2 concluiu")
    LOCK_A.release()
    LOCK_B.release()


threading.Thread(target=thread1, name="T1", daemon=True).start()
threading.Thread(target=thread2, name="T2", daemon=True).start()

time.sleep(3)
print("depois de 3 seg, ainda vivas:")
for t in threading.enumerate():
    print(" -", t.name)
