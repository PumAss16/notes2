import multiprocessing
import time
import math

def burn_cpu():
    """Функция, которая бесконечно грузит процессор математикой"""
    print(f"Ядро {multiprocessing.current_process().name} в деле!")
    while True:
        # Тяжелые операции, чтобы CPU не скучал
        for i in range(100000):
            math.sqrt(i) * math.sin(i)

def eat_memory():
    """Функция, которая ест оперативную память"""
    print("Начинаю есть память...")
    memory_hog = []
    try:
        while True:
            # Выделяем по 100 МБ каждую секунду
            memory_hog.append(bytearray(100 * 1024 * 1024))
            time.sleep(1)
    except MemoryError:
        print("Память закончилась!")

if __name__ == '__main__':
    # Узнаем, сколько у нас ядер
    cores = multiprocessing.cpu_count()
    print(f"Найдено ядер: {cores}. Запускаю нагрузку...")

    # Запускаем процесс для загрузки ВСЕХ ядер
    for _ in range(cores):
        p = multiprocessing.Process(target=burn_cpu)
        p.start()

    # Запускаем процесс, который съест память (через 5 секунд, чтобы не мешать)
    time.sleep(2)
    mem_process = multiprocessing.Process(target=eat_memory)
    mem_process.start()

    # Ждем 60 секунд и завершаем всё
    time.sleep(60)
    print("Время вышло. Останавливаю нагрузку.")