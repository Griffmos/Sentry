import multiprocessing
import concurrent.futures
import time

def do_something(t):
        print(f'sleeping for {t} sec')
        time.sleep(t)
        return (t,1)


if __name__ == '__main__':
    start = time.perf_counter()

    

    out = 'blong'
    with concurrent.futures.ProcessPoolExecutor() as executor:
        secs = [5,4,3,2,1]

        results= [executor.submit(do_something,sec ) for sec in range(10)]

        # results = executor.map(do_something, range(10))

        for f in concurrent.futures.as_completed(results):
            print(f.result())
        count =0

        # for result in results:
            # print(result)       

    

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start,2)} seconds')
