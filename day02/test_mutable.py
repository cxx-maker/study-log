a = [1,2]
b = a
b.append(3)
print("a=",a,"b=",b," |id 相同？",id(a)==id(b))
s = "hello"
t = s
t = t + "!"
print("s =",s,"t=",t,"| id 相同？", id(s) == id(t))

print(256 is 256)
print(1000 is 1000)
print(None is None)


x = 1000
y = int("1000")
print(x is y)