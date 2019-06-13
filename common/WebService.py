"""
------------------------------------
@Time : 2019/6/13 9:03
@Auth : linux超
@File : WebService.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
from suds.client import Client, WebFault


class WebService(object):
    def __init__(self):
        pass

    @staticmethod
    def get_client_obj(url):
        client = Client(url)
        service = client.service
        return service

    @staticmethod
    def send_request(url, api, data):
        """
        发送soap协议请求
        :param url: 接口地址
        :param api: 接口名称
        :param data: 请求参数
        :return: 响应信息
        """
        service = WebService.get_client_obj(url)
        my_api = getattr(service, api)
        try:
            response = my_api(data)
        except WebFault as e:
            response = e.fault
            return response
        else:
            return response


if __name__ == '__main__':
    # send_code_url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl '
    register_url = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
    # send_parm = {"client_ip": "129.45.6.7", "tmpl_id": '1', "mobile": "13691579846"}
    register_parm = {'verify_code': '639002', 'user_id': 'linuxchao',
                     'channel_id': '1', 'pwd': '123456', 'mobile': '13691579846', 'ip': '129.45.6.7'}
    web = WebService()
    # result = web.send_request(send_code_url, 'sendMCode', send_parm)
    result = web.send_request(register_url, 'userRegister', register_parm)
    print(result)
