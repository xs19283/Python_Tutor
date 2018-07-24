class add():

    def __init__(self):
        pass

    def add(self, a, b):
        print()
        return a + b


a = add()

print(a.add(1, 2))
"""
try:
    while 1:
        print(0)
except KeyboardInterrupt:
    print(123)
"""
f = open("555.txt",'a+')
print(type(f))
fvalue =f.readline()
print(fvalue)
f.write(" 222")
