import math


def compute_distance(x1, y1, x2, y2):
    d = math.sqrt(math.pow(x1-x2, 2)+math.pow(y1-y2, 2))
    return d


n = int(input("Enter no. of test cases: "))
i = 0
while i < n:
    x1, y1, x2, y2 = [float(a) for a in input().split(" ")]
    print(f"Distance: {round(compute_distance(x1,y1,x2,y2),2)}")
    i += 1
