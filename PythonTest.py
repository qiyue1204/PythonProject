# -*- coding: utf-8 -*-
"""
# Day1:Python内置支持复数及其运算，但以带括号的形式来表示复数
x=3+4j
y=5+6j

print x+y
"""

def f1(a):
    return a+2
print 'map结果为：%s '%map(f1,[1,2,3,4,5])


def f2(a,b):
    return a+b
print 'reduce结果为：%s '%reduce(f2,[1,2,3,4,5])