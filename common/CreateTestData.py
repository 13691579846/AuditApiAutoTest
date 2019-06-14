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


if __name__ == '__main__':
    data = CreateData()
    print(data.random_phone_num())
