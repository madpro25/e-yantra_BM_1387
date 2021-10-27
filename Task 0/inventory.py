n = int(input())
arr = {}
for i in range(n):
    l = int(input())
    for j in range(l):
        name, value = input().split(" ")
        arr[name] = int(value)

    op = int(input())
    for k in range(op):
        opname, name, value = input().split(" ")
        if opname == "ADD":
            if name in arr:
                arr[name] += int(value)
                print(f"UPDATED Item {name}")
            else:
                arr[name] = int(value)
                print(f"ADDED Item {name}")
        elif opname == "DELETE":
            if name in arr:
                if int(value) < arr[name]:
                    arr[name] -= int(value)
                    print(f"DELETED Item {name}")
                else:
                    print(f"Item {name} could not be deleted")
            else:
                print(f"Item {name} does not exist")
    print(f"Total Items in Inventory: {sum([val for val in arr.values()])}")
    print(arr)
