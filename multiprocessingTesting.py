import multiprocessing
import concurrent.futures
import time

def do_something(t):
    print('sleeping for 1 sec')
    time.sleep(t)
    print('done sleeping')

if __name__ == '__main__':
    start = time.perf_counter()
    
    processes = []

    for _ in range(200):
        p=multiprocessing.Process(target=do_something, args=[2])
        p.start()
        processes.append(p)
    
    for process in processes:
        process.join()


    finish = time.perf_counter()

    print(f'Finished in {round(finish-start,2)} seconds')
