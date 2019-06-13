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
from common.DataReplace import do_replace


@ddt
class TestSendCode(unittest.TestCase):

    values = do_excel.get_all_values('sendMCode')

    @classmethod
    def setUpClass(cls):
        cls.web_service = WebService()

    @data(*values)
    def test_send_code(self, value):
        case_id = value.CaseId
        case_title = value.Title
        case_url = value.URL
        case_data = value.Data
        api_name = value.ApiName
        case_expected = value.Expected
        request_url = do_config("Project", "Url") + case_url
        case_data = do_replace.parameters_phone(case_data)
        response = self.web_service(request_url, api_name, case_data)
        print(type(response))
        # try:
        #     self.assertEqual(case_expected, response, msg="用例[{}]测试失败".format(case_title))
        # except AssertionError:


    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
