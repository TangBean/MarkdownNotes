#cpython中垃圾回收的算法是采用 引用计数
a = object()
b = a
del a
print(b)
print(a)
class A:
    def __del__(self):
        pass
