#python和java中的变量本质不一样，python的变量实质上是一个指针 int str， 便利贴

a = 1
a = "abc"
#1. a贴在1上面
#2. 先生成对象 然后贴便利贴

a = [1,2,3]
b = a
print (id(a), id(b))
print (a is b)
# b.append(4)
# print (a)

a = [1,2,3,4]
b = [1,2,3,4]

class People:
    pass

person = People()
if type(person) is People:
    print ("yes")
# print(a == b)
# print (id(a), id(b))
# print (a is b)
