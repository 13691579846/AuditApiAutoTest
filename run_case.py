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

from libs import HTMLTestRunnerNew
from config.config import (ENVIRONMENT, REPORT_DIR, CASE_DIR)
from common.CreatePath import ModelsClass



def tc_suite():
    """测试套件"""
    discover = unittest.defaultTestLoader.discover(CASE_DIR, 'test_*.py')
    return discover


if __name__ == '__main__':

    report_dir = ModelsClass.create_dir(REPORT_DIR)
    report_file_name = ModelsClass.file_name('html')
    with open(report_dir + '/' + report_file_name, 'wb') as f:
        runner = HTMLTestRunnerNew.HTMLTestRunner(stream=f,
                                                  description=ENVIRONMENT,
                                                  title='接口自动化测试项目报告',
                                                  tester='Linux超',
                                                  verbosity=2)
        runner.run(tc_suite())