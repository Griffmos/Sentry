
import numpy


myList:list

def changeList(index:int):
    myList[index]+=1

def changeThisList(index:int, list:list):
    list[index]+=1

if (__name__=='__main__'):

    #declaring up there is like making static
    myList=numpy.zeros(5,int)

    changeList(1)

    print(myList)

    newArray=numpy.ones(6, int)

    print(f'newArray before: {newArray}')

    changeThisList(2, newArray)
    print(f'newArray after: {newArray}')




