import multiprocessing
import time

class ClockProcess(multiprocessing.Process):
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval
        self.data = [1,2,3]

    def set_data(self, data):
        self.data = data

    def run(self):
        n = 5
        while n > 0:
            print(f"data is {self.data}")
            time.sleep(self.interval)
            n -= 1

if __name__ == '__main__':
    p = ClockProcess(0.5)
    p.start() 

    data = [1, 2]
    while p.is_alive():        
        time.sleep(0.5)
        p.set_data(data)
        data *= 2
