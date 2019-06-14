"""
------------------------------------
@Time : 2019/6/14 9:28
@Auth : linux超
@File : CreateTestData.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import random
import string

from common.HandleMysql import HandleMysql


class CreateData(object):

    @staticmethod
    def random_phone_num():
        """随机一个电话号码"""
        num_start = ['134', '135', '136', '137', '138',
                     '139', '150', '151', '152', '158',
                     '159', '157', '182', '187', '188',
                     '147', '130', '131', '132', '155',
                     '156', '185', '186', '133', '153',
                     '180', '189']
        start = random.choice(num_start)
        end = ''.join(random.sample(string.digits, 5))
        phone_number = start + end + '846'
        return phone_number

    @staticmethod
    def is_exist_db(phone):
        mysql = HandleMysql()
        sql = 'SELECT Fmobile_no FROM sms_db_46.t_mvcode_info_8 where Fmobile_no=%s;'
        exist = mysql(sql=sql, args=(phone,))
        mysql.close()
        if exist:
            return True
        else:
            return False

    @staticmethod
    def get_unregistered_phone():
        """获取未注册的手机号"""
        while 1:
            phone = CreateData.random_phone_num()
            if not CreateData.is_exist_db(phone):
                break
        return phone


if __name__ == '__main__':
    data = CreateData()
    print(data.random_phone_num())
    print(data.get_unregistered_phone())
