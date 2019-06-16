"""
------------------------------------
@Time : 2019/6/15 19:58
@Auth : linux超
@File : test_3_verifyUserAuth.py
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


@ddt
class TestVerifyUserAuth(unittest.TestCase):
    """实名认证接口"""
    values = do_excel.get_all_values('verifyUserAuth')

    @classmethod
    def setUpClass(cls):
        print('开始执行[{}]测试用例'.format(cls.__doc__))
        cls.mysql = HandleMysql()
        # 执行认证接口之前先删除表中已经认证的身份证号
        cls.mysql(sql='delete FROM user_db.t_user_auth_info where Ftrue_name in ("超哥", "张亮");')
        # 取已经注册的uid
        uid_sql = \
            'SELECT Fuid FROM user_db.t_user_info where Ftrue_name is null and Fuser_id like "linux超%" limit 1;'
        uid = str(cls.mysql(uid_sql)["Fuid"])
        if not uid:
            raise EnvironmentError("数据库中不存在已经注册的uid,请先注册!")
        setattr(DataReplace, 'uid', uid)

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
        # 验证实名认证成功时， 是否是有效的认证(姓名和身份证不匹配时是无效的认证)
        if sql:
            case_data = HandleJson.json_to_dict(case_data)
            true_name = case_data["true_name"]  # 认证成功时的真实姓名
            setattr(DataReplace, "true_name", true_name)
            sql = DataReplace.parameters_verify_user_auth_api(sql)
            flstate = str(self.mysql(sql)["Flstate"])
            if flstate == "1":
                actual_dict["Flstate"] = "有效"
            else:
                actual_dict["Flstate"] = "无效"
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
        cls.mysql.close()
        print('结束执行[{}]测试用例'.format(cls.__doc__))


if __name__ == '__main__':
    unittest.main()
