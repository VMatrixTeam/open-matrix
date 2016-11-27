from src.producer.producer import *
from src.worker.worker import *
if __name__ == '__main__':
    p = Producer()
    w = Worker(1)
    p.start()
    w.start()
    p.join()
    w.join()
