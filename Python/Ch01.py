d = {1: [1, 2, 3]}
li = d[1]
for i in li:
    if i == 1:
        print(i)


def printName(a):
    print(a)



printName(123)


gds = {1: "are", 4: "you", 3: "ready"}

print(gds[4])

dfg = {}
for i in range(0, 5):
    key = int(input("你的KEY: "))
    value = int(input("你的值: "))
    dfg[key] = value

print(dfg)

for i in range(0, 5):
    g = int(input())
    print(dfg.get(g, "沒有找到"))
    print()

