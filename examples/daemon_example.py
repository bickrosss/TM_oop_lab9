from multiprocessing import Process
from time import sleep

def func(name):
    counter = 0
    while True:
        print(f"proc {name}, counter = {counter}")
        counter += 1
        sleep(0.1)

if __name__ == "__main__":
    # Указание на то, что процесс демон при создании объекта класса Process
    proc1 = Process(target=func, args=("proc1",), daemon=True)
    # Указание на то, что процесс демон через свойство daemon
    proc2 = Process(target=func, args=("proc2",))
    proc2.daemon = True

    # Запуск процессов
    proc1.start()
    proc2.start()
    sleep(0.3)

    # Процессы proc1 и proc2 завершаться вместе с родительским процессом
    # ...
