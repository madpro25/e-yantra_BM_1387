def pattern(n):
    s = ""
    for i in range(n):
        if i == 0:
            s += f"{i+3}"
        elif i % 2 == 1:
            s += f" {i*i}"
        else:
            s += f" {2*i}"

    print(s)


n = int(input("Enter no. of test cases: "))
i = 0
while i < n:
    pattern(int(input()))
    i += 1
