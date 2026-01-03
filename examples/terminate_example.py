from multiprocessing import Process  
from time import sleep  

def func():  
    counter = 0  
    while True:  
        print(f"counter = {counter}")  
        counter += 1  
        sleep(0.1)  

if __name__ == "__main__":  
    proc = Process(target=func)  
    proc.start()  
    sleep(0.7)  
    proc.terminate()
