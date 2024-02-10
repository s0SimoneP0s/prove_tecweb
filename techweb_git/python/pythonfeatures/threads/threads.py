import threading
import time

def func(a):
    print("Ciao! sono il thread " + threading.current_thread().name + "dormiro per " + str(a) + " secs")
    time.sleep(a)
    print(threading.current_thread().name+": ho finito di dormire")


if __name__ == "__main__":
    NUM_THREADS = 2

    print("Sono il " + threading.current_thread().name  + " e gestiro " + str(NUM_THREADS) + " threads")

    l = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=func, args=(i+1,))
        t.start()
        l.append(t)

    for t in l: 
        t.join()

    print(threading.current_thread().name  + " ho finito di aspettare i threads")
