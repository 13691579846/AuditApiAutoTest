"""
------------------------------------
@Time : 2019/6/14 11:14
@Auth : linux超
@File : base.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import unittest


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('开始执行[{}]测试用例'.format(cls.__doc__))


    @classmethod
    def tearDownClass(cls):
        print('结束执行[{}]测试用例'.format(cls.__doc__))