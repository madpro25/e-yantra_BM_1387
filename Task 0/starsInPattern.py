def pattern(x):
    s = ""
    for i in range(x, 0, -1):
        s = ""
        for j in range(1, i+1):
            if j % 5 != 0:
                s += "*"
            else:
                s += "#"
        print(s)


n = int(input("Enter no. of test cases: "))
for i in range(n):
    pattern(int(input()))
