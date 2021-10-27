n = []
s = []
for _ in range(int(input())):
    name, score = input().split(" ")
    n.append(name)
    s.append(float(score))
a = max(s)
b = min(s)
for i in range(len(n)):
    if s[i] == a and s[i] > b:
        a = s[i]

for j in range(len(n)):
    if s[j] == a:
        print(n[j])
