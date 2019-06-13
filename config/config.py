"""
------------------------------------
@Time : 2019/6/13 8:59
@Auth : linux超
@File : config.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import os

"""
All dirs of the project
"""
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUSINESS_DIR = os.path.join(PROJECT_DIR, 'business')
CASE_DIR = os.path.join(PROJECT_DIR, 'cases')
COMMON_DIR = os.path.join(PROJECT_DIR, 'common')
CONFIG_DIR = os.path.join(PROJECT_DIR, 'config')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
LIBS_DIR = os.path.join(PROJECT_DIR, 'libs')
"""
All files path of the project
"""
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.ini')
DATA_PATH = os.path.join(DATA_DIR, 'testcases.xlsx')


if __name__ == '__main__':
    print(CONFIG_PATH)
    print(DATA_PATH)
