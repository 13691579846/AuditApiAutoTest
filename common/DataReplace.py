"""
------------------------------------
@Time : 2019/6/13 9:02
@Auth : linux超
@File : DataReplace.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import re


class DataReplace(object):
    """正则表达式"""
    pattern_phone = re.compile(r'\$\{phone\}')

    def __init__(self):
        pass

    @staticmethod
    def replace(pattern, data, source):
        """匹配到正则表达式替换数据"""
        if isinstance(data, str):
            if re.search(pattern, source):
                source = re.sub(pattern, data, source)
            return source
        else:
            raise TypeError("data '{}' must be string".format(data))

    @classmethod
    def replace_phone(cls, source):
        """替换数据"""
        phone = '13691579846'
        source = cls.replace(cls.pattern_phone, phone, source)
        return source

    @classmethod
    def parameters_phone(cls, source):
        """参数化"""
        source = cls.replace_phone(source)
        return source


if __name__ == '__main__':
    source_data = '{"mobilephone": ${phone}, "pwd": "123456"}'
    do_replace = DataReplace()
    print(do_replace.parameters_phone(source_data))
