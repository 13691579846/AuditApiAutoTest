"""
------------------------------------
@Time : 2019/6/14 21:54
@Auth : linux超
@File : test.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
value = '{"client_ip":"192.168.1.1", "tmpl_id": "1","mobile":"13956784846"}'
new_value = eval(value)
print(new_value)