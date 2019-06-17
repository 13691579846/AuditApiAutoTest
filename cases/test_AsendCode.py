"""
------------------------------------
@Time : 2019/6/13 9:00
@Auth : linux超
@File : test_AsendCode.py
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
from common.HandleJson import HandleJson
from common.RecordLog import logger


@ddt
class TestSendCodeApi(unittest.TestCase):
    """发送短信验证码接口"""
    values = do_excel.get_all_values('sendMCode')

    @classmethod
    def setUpClass(cls):
        logger.info('------开始加载[{}]测试用例------'.format(cls.__doc__))

    def setUp(self):
        logger.info('*开始执行[{}]测试用例*'.format(self.id()))

    @data(*values)
    def test_send_code(self, value):
        case_id = value.CaseId
        case_title = value.Title
        case_url = value.URL
        case_data = value.Data
        api_name = value.ApiName
        case_expected = HandleJson.json_to_dict(value.Expected)
        request_url = do_config("Project", "Url") + case_url
        case_data = DataReplace.parameters_verify_code_api(case_data)
        response = WebService.send_request(request_url, api_name, case_data)
        actual_dict = dict(response)
        actual_str = str(actual_dict)
        try:
            logger.info("测试用例执行实际结果为:[{}]".format(actual_str))
            do_excel.write_cell("sendMCode", case_id + 1, 8, actual_str)
            self.assertEqual(case_expected, actual_dict, msg='用例[{}]测试失败'.format(case_title))
        except AssertionError as e:
            do_excel.write_cell("sendMCode", case_id+1, 9, 'Fail', color='red')
            logger.error("测试用例[{}]执行结果:{}\n具体原因信息:{}".format(case_title, "Fail", e))
            raise e
        else:
            do_excel.write_cell("sendMCode", case_id+1, 9, 'Pass', color='green')
            logger.error("测试用例[{}]执行结果:{}".format(case_title, "Pass"))

    def tearDown(self):
        logger.info('*结束执行[{}]测试用例*'.format(self.id()))

    @classmethod
    def tearDownClass(cls):
        logger.info('------结束加载[{}]测试用例------'.format(cls.__doc__))


if __name__ == '__main__':
    unittest.main()
