from multiprocessing import Process, Queue, Lock
import time
import os

q = Queue(10)

def worker(identifier, queue, lock):
    prefix = "[worker {0}:{1}]".format(identifier, os.getpid())
    while True:
        time.sleep(4)
        task = queue.get()
        lock.acquire()
        print prefix, task
        lock.release()

def producer(identifier, queue, lock):
    prefix = "[producer {0}:{1}]".format(identifier, os.getpid())
    while True:
        time.sleep(1)
        queue.put("this is a task")
        lock.acquire()
        print prefix, "put a task"
        lock.release()

if __name__ == '__main__':

    lock = Lock()

    p1 = Process(target=worker, args=("Bob", q, lock))
    p2 = Process(target=producer, args=("Alice", q, lock))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
