"""
------------------------------------
@Time : 2019/6/13 8:58
@Auth : linux超
@File : run_case.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import unittest

from libs import (HTMLTestRunner, ExtentHTMLTestRunner)
from config.config import (ENVIRONMENT, REPORT_DIR, LOG_DIR, CASE_DIR)
from common.CreatePath import ModelsClass
from common.ParseConfig import do_config


def tc_suite():
    """测试套件"""
    suite = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(CASE_DIR, 'test_*.py')
    suite.addTest(discover)
    return suite


# TODO: Optimizing code
# TODO: add log
if __name__ == '__main__':
    ModelsClass.create_dir(LOG_DIR)
    report_dir = ModelsClass.create_dir(REPORT_DIR)
    report_file_name = ModelsClass.file_name('html')
    # 第一种测试报告
    with open(report_dir + '/' + report_file_name, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestReportCN(stream=f,
                                                 description=ENVIRONMENT,
                                                 title=do_config('Project', 'Name'),
                                                 tester=do_config('Project', 'Tester'),
                                                 verbosity=2)
        runner.run(tc_suite())
    # 第二种测试报告
    # with open(report_dir + '/' + report_file_name, 'wb') as f:
    #     runner = ExtentHTMLTestRunner.HTMLTestRunner(stream=f,
    #                                                  description=ENVIRONMENT,
    #                                                  title=do_config('Project', 'Name'),
    #                                                  verbosity=2)
    #     runner.run(tc_suite())
