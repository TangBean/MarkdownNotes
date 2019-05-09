#我们去检查某个类是否有某种方法
class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list

    def __len__(self):
        return len(self.employee)


com = Company(["bobby1","bobby2"])
print(hasattr(com, "__len__"))


class A:
    pass

class B:
    pass

#我们在某些情况之下希望判定某个对象的类型
from collections.abc import Sized
isinstance(com, Sized)

b = B()
print(isinstance(b, A))
# print(len(com))

#我们需要强制某个子类必须实现某些方法
#实现了一个web框架，集成cache(redis, cache, memorychache)
#需要设计一个抽象基类， 指定子类必须实现某些方法

#如何去模拟一个抽象基类

import abc
from collections.abc import *


class CacheBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def set(self, key, value):
        pass
# class CacheBase():
#     def get(self, key):
#         raise NotImplementedError
#     def set(self, key, value):
#         raise NotImplementedError
#
class RedisCache(CacheBase):
    def set(self, key, value):
        pass

# redis_cache = RedisCache()
# redis_cache.set("key", "value")
