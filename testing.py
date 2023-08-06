print("Hello world!")

list = ["hi", "im", "griffin"]

for i in range(len(list)):
    print(list[i])

list2d = [[1,2,3],[4,5,6],[7,8,9]]

for r in range(len(list2d)):
    for c in range(len(list2d[0])):
        print(list2d[r][c], end="")
    print()