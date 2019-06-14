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
from common.CreateTestData import CreateData


class DataReplace(object):
    """正则表达式"""
    pattern_unregistered_phone = re.compile(r'\$\{verify_phone\}')
    pattern_verify_unregistered_phone = re.compile(r'\$\{verify_unregistered_phone\}')
    pattern_verify_code = re.compile(r'\$\{verify_code\}')
    pattern_verify_registered_phone = re.compile(r'\$\{verify_registered_phone\}')

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
    def replace_verify_phone(cls, source):
        verify_phone = CreateData.random_phone_num()  # 随机一个尾号为846的手机号
        source = cls.replace(cls.pattern_unregistered_phone, verify_phone, source)
        return source

    @classmethod
    def replace_verify_unregistered_phone(cls, source):
        if hasattr(DataReplace, 'verify_unregistered_phone'):
            # 未注册且对应发送了验证码的手机号(取数据库中未注册的)
            verify_unregistered_phone = getattr(cls, 'verify_unregistered_phone')
            source = cls.replace(cls.pattern_verify_unregistered_phone, verify_unregistered_phone, source)
        else:
            source = cls.replace(cls.pattern_verify_unregistered_phone, '', source)
        return source

    @classmethod
    def replace_verify_code(cls, source):
        # 数据库中取验证码
        if hasattr(cls, 'verify_code'):
            verify_code = getattr(cls, 'verify_code')
            source = cls.replace(cls.pattern_verify_code, verify_code, source)
        else:
            source = cls.replace(cls.pattern_verify_code, '', source)
        return source

    @classmethod
    def replace_verify_registered_phone(cls, source):
        verify_registered_phone = '13691579846'  # 取数据库中已注册的手机号
        source = cls.replace(cls.pattern_verify_registered_phone, verify_registered_phone, source)
        return source

    @classmethod
    def parameters_verify_code_api(cls, source):
        source = cls.replace_verify_phone(source)
        return source

    @classmethod
    def parameters_register_api(cls, source):
        source = cls.replace_verify_phone(source)
        source = cls.replace_verify_unregistered_phone(source)
        source = cls.replace_verify_code(source)
        source = cls.replace_verify_registered_phone(source)
        return source


if __name__ == '__main__':
    source_data = '{"mobilephone": ${phone}, "pwd": "123456"}'
    do_replace = DataReplace()
    print(do_replace.parameters_verify_code_api(source_data))
