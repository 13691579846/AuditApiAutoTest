"""
------------------------------------
@Time : 2019/6/14 20:11
@Auth : linux超
@File : test_userRegister.py
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
class TestSendCode(Base):
    """用户注册接口"""
    values = do_excel.get_all_values('userRegister')

    verify_unregistered_phone = CreateData.get_unregistered_phone()
    setattr(DataReplace, 'verify_unregistered_phone', verify_unregistered_phone)
    print(verify_unregistered_phone)


    @data(*values)
    def test_send_code(self, value):
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
        print(response)
        # if sql:
        #     sql = DataReplace.parameters_register_api(sql)
        #     mysql = HandleMysql()
        #     verify_code = str(mysql(sql=sql)["Fverify_code"])
        #     setattr(DataReplace, 'verify_code', verify_code)
        #     mysql.close()
        # actual_dict = dict(response)
        # print(actual_dict)
        # actual_str = str(actual_dict)
        # print(actual_str)
        # do_excel.write_cell('userRegister', case_id+1, 8, actual_str)
        # try:
        #     self.assertEqual(case_expected, actual_dict, msg='用例[{}]测试失败'.format(case_title))
        # except AssertionError as e:
        #     do_excel.write_cell('userRegister', case_id+1, 9, 'Fail', color='red')
        #     raise e
        # else:
        #     do_excel.write_cell('userRegister', case_id+1, 9, 'Pass', color='green')


if __name__ == '__main__':
    unittest.main()
