
import concurrent.futures
import numpy
import time


#doesn't work at all


nums=numpy.zeros(100)

def changeList(index):
    nums[index]+=1
    print(nums)
    return 

if (__name__ == '__main__'):


    with concurrent.futures.ProcessPoolExecutor() as executor:


        results = executor.map(changeList, range(0,100,2))

        
        for result in results:
            print('done')       