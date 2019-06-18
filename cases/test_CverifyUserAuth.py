"""
------------------------------------
@Time : 2019/6/15 19:58
@Auth : linux超
@File : test_CverifyUserAuth.py
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
from common.HandleMysql import HandleMysql
from common.CreateTestData import CreateData
from common.RecordLog import logger


@ddt
class TestVerifyUserAuth(unittest.TestCase):
    """实名认证接口"""
    values = do_excel.get_all_values(do_config("Excel", "verifyUserAuthApi"))

    @classmethod
    def setUpClass(cls):
        logger.info('---开始加载[{}]测试用例---'.format(cls.__doc__))
        cls.mysql = HandleMysql()
        # 执行认证接口之前先删除表中已经认证的身份证号
        cls.mysql(sql='delete FROM user_db.t_user_auth_info where Ftrue_name in ("超哥", "张亮");')
        cls.verify_unregistered_phone = CreateData.get_unregistered_phone()
        setattr(DataReplace, 'verify_unregistered_phone', cls.verify_unregistered_phone)

    def setUp(self):
        logger.info('*开始执行[{}]测试用例*'.format(self.id()))

    @data(*values)
    def test_verify_user_auth(self, value):
        case_id = value.CaseId
        case_title = value.Title
        case_url = value.URL
        case_data = value.Data
        api_name = value.ApiName
        sql = value.Sql
        case_expected = HandleJson.json_to_dict(value.Expected)
        request_url = do_config("Project", "Url") + case_url
        case_data = DataReplace.parameters_verify_user_auth_api(case_data)
        response = WebService.send_request(request_url, api_name, case_data)
        actual_dict = dict(response)
        if sql and api_name == "sendMCode":
            code_sql = DataReplace.parameters_verify_user_auth_api(sql)
            verify_code = str(self.mysql(sql=code_sql)["Fverify_code"])
            setattr(DataReplace, 'verify_code', verify_code)
        if sql and api_name == "userRegister":
            case_data = HandleJson.json_to_dict(case_data)
            user_name = case_data["user_id"]
            setattr(DataReplace, "user_name", user_name)
            registered_uid_sql = DataReplace.parameters_verify_user_auth_api(sql)
            registered_uid = str(self.mysql(registered_uid_sql)["Fuid"])
            setattr(DataReplace, "uid", registered_uid)
        # 验证实名认证成功时， 是否是有效的认证(姓名和身份证不匹配时是无效的认证)
        if sql and api_name == "verifyUserAuth":
            case_data = HandleJson.json_to_dict(case_data)
            true_name = case_data["true_name"]  # 认证成功时的真实姓名
            setattr(DataReplace, "true_name", true_name)
            sql = DataReplace.parameters_verify_user_auth_api(sql)
            state = str(self.mysql(sql)["Flstate"])
            if state == "1":
                actual_dict["Flstate"] = "有效"
            else:
                actual_dict["Flstate"] = "无效"
        actual_str = str(actual_dict)
        try:
            logger.info("测试用例执行实际结果为:[{}]".format(actual_str))
            do_excel.write_cell(do_config("Excel", "verifyUserAuthApi"),
                                case_id + 1,
                                do_config("Excel", "actual_column"),
                                actual_str)
            self.assertEqual(case_expected, actual_dict, msg='用例[{}]测试失败'.format(case_title))
        except AssertionError as e:
            do_excel.write_cell(do_config("Excel", "verifyUserAuthApi"),
                                case_id+1,
                                do_config("Excel", "result_column"),
                                'Fail',
                                color='red')
            logger.error("测试用例[{}]执行结果:{}\n具体原因信息:{}".format(case_title, "Fail", e))
            raise e
        else:
            do_excel.write_cell(do_config("Excel", "verifyUserAuthApi"),
                                case_id+1,
                                do_config("Excel", "result_column"),
                                'Pass',
                                color='green')
            logger.error("测试用例[{}]执行结果:{}".format(case_title, "Pass"))

    def tearDown(self):
        logger.info('*结束执行[{}]测试用例*'.format(self.id()))

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()
        logger.info('---结束加载[{}]测试用例---'.format(cls.__doc__))


if __name__ == '__main__':
    unittest.main()
