def decToBin(n, a):
    if n == 0:
        return a
    a += decToBin(n//2, f"{n%2}")
    return a


n = int(input("Enter number of test cases: "))
for i in range(n):
    res = decToBin(int(input()), "")
    print('0'*(8-len(res))+res[::-1])
