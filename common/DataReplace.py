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
    pattern_user_id = re.compile(r'\$\{user_id\}')
    pattern_registered_uid = re.compile(r'\$\{registered_uid\}')
    pattern_true_name = re.compile(r'\$\{true_name\}')

    pattern_trued_uid = re.compile(r'\$\{trued_uid\}')
    pattern_untrue_register_uid = re.compile(r'\$\{untrue_register_uid\}')

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
        """随机一个尾号为846的手机号"""
        verify_phone = CreateData.random_phone_num()
        source = cls.replace(cls.pattern_unregistered_phone, verify_phone, source)
        return source

    @classmethod
    def replace_verify_unregistered_phone(cls, source):
        """未注册且对应发送了验证码的手机号(取数据库中未注册的)"""
        if hasattr(DataReplace, 'verify_unregistered_phone'):
            verify_unregistered_phone = getattr(cls, 'verify_unregistered_phone')
            source = cls.replace(cls.pattern_verify_unregistered_phone, verify_unregistered_phone, source)
        else:
            source = cls.replace(cls.pattern_verify_unregistered_phone, '', source)
        return source

    @classmethod
    def replace_verify_code(cls, source):
        """数据库中取验证码"""
        if hasattr(cls, 'verify_code'):
            verify_code = getattr(cls, 'verify_code')
            source = cls.replace(cls.pattern_verify_code, verify_code, source)
        else:
            source = cls.replace(cls.pattern_verify_code, '', source)
        return source

    @classmethod
    def replace_user_id(cls, source):
        """注册成功之后需要根据user_id查询数据库是否有了真实的注册信息"""
        if hasattr(cls, 'user_name'):
            user_id = getattr(cls, 'user_name')
            source = cls.replace(cls.pattern_user_id, user_id, source)
        else:
            source = cls.replace(cls.pattern_user_id, '', source)
        return source

    @classmethod
    def replace_registered_uid(cls, source):
        """获取已经注册的uid"""
        if hasattr(cls, 'uid'):
            registered_uid = getattr(cls, 'uid')
            source = cls.replace(cls.pattern_registered_uid, registered_uid, source)
        else:
            source = cls.replace(cls.pattern_registered_uid, '', source)
        return source

    @classmethod
    def replace_true_name(cls, source):
        """从数据库中判断认证成功后是否是有效的认证"""
        if hasattr(cls, "true_name"):
            true_name = getattr(cls, "true_name")
            source = cls.replace(cls.pattern_true_name, true_name, source)
        else:
            source = cls.replace(cls.pattern_true_name, '', source)
        return source

    @classmethod
    def replace_trued_uid(cls, source):
        """替换已实名的uid"""
        if hasattr(cls, 'trued_uid'):
            trued_uid = getattr(cls, 'trued_uid')
            source = cls.replace(cls.pattern_trued_uid, trued_uid, source)
        else:
            source = cls.replace(cls.pattern_trued_uid, '', source)
        return source

    @classmethod
    def replace_untrue_register_uid(cls, source):
        """替换未实名的uid"""
        if hasattr(cls, "untrue_register_uid"):
            untrue_register_uid = getattr(cls, "untrue_register_uid")
            source = cls.replace(cls.pattern_untrue_register_uid, untrue_register_uid, source)
        else:
            source = cls.replace(cls.pattern_untrue_register_uid, '', source)
        return source

    @classmethod
    def parameters_verify_code_api(cls, source):
        """参数化发送验证码接口"""
        source = cls.replace_verify_phone(source)
        return source

    @classmethod
    def parameters_register_api(cls, source):
        """参数化注册接口"""
        source = cls.replace_verify_phone(source)
        source = cls.replace_verify_unregistered_phone(source)
        source = cls.replace_verify_code(source)
        source = cls.replace_user_id(source)
        return source

    @classmethod
    def parameters_verify_user_auth_api(cls, source):
        """参数化实名认证接口"""
        source = cls.replace_verify_unregistered_phone(source)
        source = cls.replace_verify_code(source)
        source = cls.replace_registered_uid(source)
        source = cls.replace_user_id(source)
        source = cls.replace_true_name(source)
        return source

    @classmethod
    def parameters_bind_bank_card_api(cls, source):
        """参数化绑定银行卡接口"""
        source = cls.replace_verify_unregistered_phone(source)
        source = cls.replace_trued_uid(source)
        source = cls.replace_verify_code(source)
        source = cls.replace_user_id(source)
        source = cls.replace_untrue_register_uid(source)
        return source


if __name__ == '__main__':
    source_data = '{"mobilephone": ${phone}, "pwd": "123456"}'
    do_replace = DataReplace()
    print(do_replace.parameters_verify_code_api(source_data))
