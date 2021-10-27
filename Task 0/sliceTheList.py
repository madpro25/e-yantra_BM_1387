def sliceShow(a):
    print(" ".join(list(str(i) for i in a[::-1])))
    print(" ".join(list(str(i+3) for i in a[::3][1:])))
    print(" ".join(list(str(i-7) for i in a[::5][1:])))
    print(sum(a[3:8]))


n = int(input())
for i in range(n):
    length = int(input())
    arr = list(map(int, input().split(" ")))
    sliceShow(arr)
    i += 1
