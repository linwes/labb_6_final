import os
import psutil
import platform
from datetime import datetime
from time import sleep
import numpy as np
import concurrent.futures
import multiprocessing
import time

#key_not_found = multiprocessing.Value('i', True)

def init_globals(key_not_found, svar, key_found):
    global KEY_NOT_FOUND
    KEY_NOT_FOUND = key_not_found
    global SVAR
    SVAR = svar
    global KEY_FOUND
    KEY_FOUND = key_found
    # global WAIT
    
    
    
def pw_crack(cpu, cur_key, end_key):
    # while True:
    #     time.sleep(0.02)
    #     if WAIT.value == cpu-1:
    print(f'\tCPU: {cpu} keyspace start at {cur_key} and end at {end_key}')
    #         break
    tested = 0
    while KEY_NOT_FOUND.value and (cur_key <= end_key):
        if cur_key == SVAR:
            KEY_NOT_FOUND.value = False
            KEY_FOUND.value = cur_key
            print('')
            return f'\n\tCPU: {cpu} Tested {tested} keys Found key: {cur_key}', tested
        cur_key +=1
        tested += 1
    return f'\tCPU: {cpu} Tested {tested} keys', tested
            
     
def hacking_pw(svar):
    key_not_found = multiprocessing.Value('i', True)
    cpu_count = psutil.cpu_count(logical=True)
    key_found = multiprocessing.Value('i', 0)
    key_range = int(4294967295/cpu_count)
    tested_codes = 0
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
    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count, initializer=init_globals, initargs=(key_not_found, svar, key_found)) as executor:
        for result in executor.map(pw_crack, cpus, start_keys, end_keys):
            results.append(result[0])
            tested_codes += result[1]
            executor.shutdown()
            
    stop = time.perf_counter()
    elapsed = stop - start    
    code = key_found.value
    for i in results:
        print(i)
    print('\tDONE!')
    print(f'\tCode: {code}')
    print(f'\tCodes tested: {tested_codes}')
    print(f'\tCode found in {elapsed:0.2f} seconds')
     
    
def cpu_info():
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")

def main ():
    #cpu_info()
    svar = int(input('\nSkriv in ett tal du vill ska bli cracked:'))
    hacking_pw(svar)

if __name__ == '__main__':
    main()
