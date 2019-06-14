"""
------------------------------------
@Time : 2019/6/13 9:00
@Auth : linux超
@File : test_SendCode.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import unittest

from libs.ddt import (ddt, data)
from common.ParseExcel import do_excel
from common.ParseConfig import do_config
from common.WebService import WebService
from common.DataReplace import DataReplace
from common.CreateTestData import CreateData
from common.HandleJson import HandleJson


@ddt
class TestSendCode(unittest.TestCase):

    values = do_excel.get_all_values('sendMCode')

    @classmethod
    def setUpClass(cls):
        print('{:=^40}'.format('开始执行[发送短信验证码接口]测试用例'))
        cls.web_service = WebService()

    @data(*values)
    def test_send_code(self, value):
        case_id = value.CaseId
        case_title = value.Title
        case_url = value.URL
        case_data = value.Data
        api_name = value.ApiName
        case_expected = HandleJson.json_to_python(value.Expected)
        unregistered_phone = CreateData.random_phone_num()
        setattr(DataReplace, 'unregistered_phone', unregistered_phone)
        request_url = do_config("Project", "Url") + case_url
        case_data = DataReplace.parameters_phone(case_data)
        response = self.web_service(request_url, api_name, case_data)
        actual_dict = dict(response)
        actual_str = str(actual_dict)
        do_excel.write_cell(api_name, case_id+1, 8, actual_str)
        try:
            self.assertEqual(case_expected, actual_dict, msg='用例[{}]测试失败'.format(case_title))
        except AssertionError as e:
            do_excel.write_cell(api_name, case_id+1, 9, 'Fail', color='red')
            raise e
        else:
            do_excel.write_cell(api_name, case_id+1, 9, 'Pass', color='green')

    @classmethod
    def tearDownClass(cls):
        print('{:=^40}'.format('结束执行[发送短信验证码接口]测试用例'))


if __name__ == '__main__':
    unittest.main()
