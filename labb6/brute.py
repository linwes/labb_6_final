import os
import psutil
import platform
from datetime import datetime
from time import sleep
import numpy as np
import concurrent.futures
import multiprocessing
import time
from random import randint
#key_not_found = multiprocessing.Value('i', True)

def init_globals(ingen_nyckel, lösenord, key_found):
    global INGEN_NYCKEL
    INGEN_NYCKEL = ingen_nyckel
    global LÖSENORD
    LÖSENORD = lösenord
    global KEY_FOUND
    KEY_FOUND = key_found
    # global WAIT
    
    
    
def crack(cpu, cur_key, end_key):
    # while True:
    #     time.sleep(0.02)
    #     if WAIT.value == cpu-1:
    print(f'CPU: {cpu} keyspace start at {cur_key} and end at {end_key}')
    #         break
    tested = 0
    while INGEN_NYCKEL.value and (cur_key <= end_key):
        if cur_key == LÖSENORD:
            INGEN_NYCKEL.value = False
            KEY_FOUND.value = cur_key
            print('')
            return f'\n\tCPU: {cpu} Tested {tested} keys Found key: {cur_key}', tested
        cur_key +=1
        tested += 1
    return f'\tCPU: {cpu} Tested {tested} keys', tested
            
     
def hack(lösenord):
    ingen_nyckel = multiprocessing.Value('i', True)
    cpu_count = psutil.cpu_count(logical=True)
    key_found = multiprocessing.Value('i', 0)
    key_range = int(4294967295/cpu_count)
    testade = 0
    cpus = []
    start_keys = []
    end_keys = []
    results = []
    
    for i in range (0, cpu_count):
        start_key = (i) * key_range
        start_keys.append(start_key)
        if i == cpu_count - 1:
            end_key = 4294967295
        else:
            end_key = (i+1) * key_range
        end_keys.append(end_key)
        cpus.append(i+1)
         
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count, initializer=init_globals, initargs=(ingen_nyckel, lösenord, key_found)) as executor:
        for result in executor.map(crack, cpus, start_keys, end_keys):
            results.append(result[0])
            testade += result[1]
            executor.shutdown()
                
    stop = time.perf_counter()
    elapsed = stop - start    
    lösen = key_found.value
    for i in results:
        print(i)
    print(f'lösenord: {lösen}')
    print(f'lösenord testade: {testade}')
    print(f'lösenordet hittades efter {elapsed:0.2f} seconds')
     
    
def cpu_info():
    print("fysiska prosesorer:", psutil.cpu_count(logical=False))
    print("antal prosesorer:", psutil.cpu_count(logical=True))
    cpufreq = psutil.cpu_freq()
    print(f"högsta frekvens: {cpufreq.max:.2f}Mhz")
    print(f"minsta frekvens: {cpufreq.min:.2f}Mhz")
    print(f"nuvarande frekvens: {cpufreq.current:.2f}Mhz")
    print("CPU användning per prosesor:")
    for i, procent in enumerate(psutil.cpu_percent(percpu=True)):
        print(f"prosessor {i}: {procent}%")
    print(f"Total CPU användning: {psutil.cpu_percent()}%")

def main ():
    lösenord  = str(randint(0,4294967295))
    hack(lösenord)

if __name__ == '__main__':
    main()
