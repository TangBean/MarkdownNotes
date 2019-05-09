from threading import Thread
class MyThread(Thread):
    def __init__(self, name, user):
        self.user = user
        super().__init__(name=name)

#既然我们重写B的构造函数， 为什么还要去调用super？
#super到底执行顺序是什么样的？


class A:
    def __init__(self):
        print ("A")

class B(A):
    def __init__(self):
        print ("B")
        super().__init__()

class C(A):
    def __init__(self):
        print ("C")
        super().__init__()
        
class D(B, C):
    def __init__(self):
        print ("D")
        super(D, self).__init__()

if __name__ == "__main__":
    print(D.__mro__)
    d = D()

#mixin模式特点
# 1. Mixin类功能单一
# 2. 不和基类关联，可以和任意基类组合， 基类可以不和mixin关联就能初始化成功
# 3. 在mixin中不要使用super这种用法