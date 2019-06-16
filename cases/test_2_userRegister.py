"""
------------------------------------
@Time : 2019/6/14 20:11
@Auth : linux超
@File : test_2_userRegister.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import unittest

from base.base import Base
from libs.ddt import (ddt, data)
from common.ParseExcel import do_excel
from common.ParseConfig import do_config
from common.WebService import WebService
from common.DataReplace import DataReplace
from common.HandleJson import HandleJson
from common.CreateTestData import CreateData
from common.HandleMysql import HandleMysql


@ddt
class TestUserRegisterApi(unittest.TestCase):
    """用户注册接口"""
    values = do_excel.get_all_values('userRegister')

    @classmethod
    def setUpClass(cls):
        print('开始执行[{}]测试用例'.format(cls.__doc__))
        cls.mysql = HandleMysql()
        cls.verify_unregistered_phone = CreateData.get_unregistered_phone()
        setattr(DataReplace, 'verify_unregistered_phone', cls.verify_unregistered_phone)

    @data(*values)
    def test_user_register(self, value):
        case_id = value.CaseId
        case_title = value.Title
        case_url = value.URL
        case_data = value.Data
        api_name = value.ApiName
        case_expected = HandleJson.json_to_dict(value.Expected)  # 期望值(字典)
        sql = value.Sql
        request_url = do_config("Project", "Url") + case_url  # 请求地址
        case_data = DataReplace.parameters_register_api(case_data)
        response = WebService.send_request(request_url, api_name, case_data)
        if sql and api_name == 'sendMCode':
            sql = DataReplace.parameters_register_api(sql)
            verify_code = str(self.mysql(sql=sql)["Fverify_code"])
            setattr(DataReplace, 'verify_code', verify_code)
        actual_dict = dict(response)
        if sql and ("is_exist_db" in case_expected.keys()):
            # 如果注册成功，去验证一下数据库 {"retCode": "0", "retInfo": "ok","is_exist_db":"yes"}
            case_data = HandleJson.json_to_dict(case_data)
            user_name = case_data["user_id"]  # 注册成功之后得到user_id 去数据库搜索对应的帐号信息
            setattr(DataReplace, 'user_name', user_name)
            sql = DataReplace.parameters_register_api(sql)
            user_info = self.mysql(sql)
            if user_info:
                actual_dict["is_exist_db"] = "yes"
            else:
                actual_dict["is_exist_db"] = "no"
        actual_str = str(actual_dict)
        do_excel.write_cell('userRegister', case_id+1, 8, actual_str)
        try:
            self.assertEqual(case_expected, actual_dict, msg='用例[{}]测试失败'.format(case_title))
        except AssertionError as e:
            do_excel.write_cell('userRegister', case_id+1, 9, 'Fail', color='red')
            raise e
        else:
            do_excel.write_cell('userRegister', case_id+1, 9, 'Pass', color='green')

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()
        print('结束执行[{}]测试用例'.format(cls.__doc__))


if __name__ == '__main__':
    unittest.main()
