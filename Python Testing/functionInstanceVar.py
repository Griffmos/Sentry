def poopooPeePee(x:int):
    print(f"you gave me {x}")
    print (f"I have {poopooPeePee.mine}")

    poopooPeePee.mine=x

def main():

    poopooPeePee.mine = 12

    poopooPeePee(5)

    poopooPeePee(4)

    print(f"poopooPeePee has {poopooPeePee.mine}")


main()