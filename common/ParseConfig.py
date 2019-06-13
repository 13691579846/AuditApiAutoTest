"""
------------------------------------
@Time : 2019/6/13 9:01
@Auth : linux超
@File : ParseConfig.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
from configparser import ConfigParser

from config.config import CONFIG_PATH


class ParseConfig(ConfigParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def get_value(self, section='DEFAULT', option=None, is_eval=False, is_bool=False):
        """get value of section / option"""
        self.read(self.filename, encoding='utf-8')
        if option is None:
            return dict(self[section])
        if isinstance(is_bool, bool):
            if is_bool:
                return self.getboolean(section, option)
        else:
            raise ValueError('{} must be type bool'.format(is_bool))
        data = self.get(section, option)
        if data.isdigit():
            data = int(data)
            return data
        try:
            data = float(data)
            return data
        except ValueError:
            pass
        if isinstance(is_eval, bool):
            if is_eval:
                data = eval(data)
                return data
        else:
            raise ValueError('{} must be type bool'.format(is_eval))
        return data

    @classmethod
    def write_config(cls, data, path):
        """write value to config
           dict =
           {
           key:{
                key: value
                }
           }
        """
        config_obj = cls(path)
        for value in data:
            config_obj[value] = data[value]
        with open(path, 'w', encoding='utf-8') as f:
            config_obj.write(f)

    def __call__(self, section='DEFAULT', option=None, is_eval=False, is_bool=False):
        return self.get_value(section=section,
                              option=option,
                              is_eval=is_eval,
                              is_bool=is_bool)


if __name__ == '__main__':
    do_config = ParseConfig(CONFIG_PATH)
    print(do_config('Project', 'Name'))
