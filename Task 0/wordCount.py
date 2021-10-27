def countWords(s):
    words = s.split(" ")
    count = list(map(str, list(map(len, words))))
    print(",".join(count))


n = int(input("Enter no. of test cases: "))
for i in range(n):
    countWords(input()[1:])
