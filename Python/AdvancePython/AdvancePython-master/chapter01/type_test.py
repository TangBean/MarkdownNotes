# -*- coding: utf-8 -*-
__author__ = 'bobby'
a=1
b="abc"
print(type(1))
print(type(int))
print(type(b))
print(type(str))

class Student:
    pass

stu = Student()
print(type(stu))
print(type(Student))
print(int.__bases__)
print(str.__bases__)
print(Student.__bases__)
print(type.__bases__)
print(object.__bases__)
print(type(object))

