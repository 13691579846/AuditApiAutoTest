import os
from datetime import datetime, date


class ModelsClass(object):
    def __init__(self):
        pass

    @staticmethod
    def get_current_time():
        """获取当前日期"""
        current_time = datetime.now().strftime(str(date.today()) + '-' + '%H-%M-%S')
        return current_time

    @staticmethod
    def get_current_date():
        """获取当前日期"""
        current_date = datetime.now().strftime(str(date.today()))
        return current_date

    @staticmethod
    def file_name(file_type):
        """日志与HTML报告文件名"""
        current_time = ModelsClass.get_current_time()
        if 'HTML' == file_type.upper():
            current_time = ModelsClass.get_current_time()
            file_name = current_time + '.' + file_type
            return file_name
        elif 'LOG' == file_type.upper():
            current_time = ModelsClass.get_current_date()
            file_name = current_time + 'testing' + '.' + file_type
            return file_name
        else:
            return current_time + '.' + file_type

    @staticmethod
    def create_dir(path):
        """创建HTML报告与日志文件存放目录"""
        if not os.path.exists(path):
            os.makedirs(path)
        return path


if __name__ == '__main__':
    print(ModelsClass.create_dir('log'))
    print(ModelsClass.create_dir('report'))
    print(ModelsClass.file_name('html'))
    print(ModelsClass.get_current_time())
