"""
------------------------------------
@Time : 2019/6/13 9:03
@Auth : linux超
@File : HandleMysql.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import pymysql
from collections.abc import Iterable

from common.ParseConfig import ParseConfig
from config.config import CONFIG_PATH


class HandleMysql(object):
    def __init__(self):
        """connect mysql"""
        self.do_config = ParseConfig(CONFIG_PATH)
        try:
            self.conn = pymysql.connect(host=self.do_config('MySql', 'Host'),
                                        user=self.do_config('MySql', 'User'),
                                        password=self.do_config('MySql', 'Password'),
                                        port=self.do_config('MySql', 'Port'),
                                        charset=self.do_config('MySql', 'Charset'),
                                        cursorclass=pymysql.cursors.DictCursor
                                        )
        except Exception as e:
            print(e)
        else:
            self.cursor = self.conn.cursor()

    def query(self, sql, args=None, is_all=False):
        """select value"""
        if isinstance(args, Iterable) or args is None:
            if self.conn:
                self.cursor.execute(sql, args=args)
                self.conn.commit()
                if isinstance(is_all, bool):
                    if is_all:
                        values = self.cursor.fetchall()
                    else:
                        values = self.cursor.fetchone()
                    return values
                else:
                    raise TypeError('default parameter "{}" must be bool'.format(is_all))
            else:
                raise ConnectionError('db connect failed get values error!')
        else:
            raise TypeError('default parameter args "{}" must be Iterable'.format(args))

    def __call__(self, sql, args=None, is_all=False):
        return self.query(sql, args=args, is_all=is_all)

    def close(self):
        """close connect and cursor"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == '__main__':
    do_config = ParseConfig(CONFIG_PATH)
    mysql = HandleMysql()
    print(mysql('select * from sms_db_46.t_mvcode_info_8;'))
    mysql.close()
