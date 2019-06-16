"""
------------------------------------
@Time : 2019/6/13 9:03
@Auth : linux超
@File : WebService.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import json
from suds.client import Client, WebFault


class WebService(object):
    def __init__(self):
        pass

    @staticmethod
    def get_client_obj(url):
        service = Client(url).service
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
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                try:
                    data = eval(data)
                except Exception as e:
                    raise e
        service = WebService.get_client_obj(url)
        my_api = getattr(service, api)
        try:
            response = my_api(data)
        except WebFault as e:
            response = e.fault
            return response
        else:
            return response

    def __call__(self, url, api, data):
        response = self.send_request(url=url, api=api, data=data)
        return response


if __name__ == '__main__':
    web = WebService()
    # send_code_url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'
    # send_parm = '{"client_ip": "192.168.1.1", "tmpl_id": [1], "mobile": "13425356846"}'
    # result = web(send_code_url, 'sendMCode', send_parm)
    register_url = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
    register_parm = {'verify_code': '117822',
                     'user_id': '超哥牛逼',
                     'channel_id': '1',
                     'pwd': '123456',
                    'pay_pwd':"123456",
                     'mobile': '13425356846',
                     "ip": '192.168.1.1'}
    result = web.send_request(register_url, 'userRegister', register_parm)

    # user_verify_url = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
    # user_verify_parm = {"uid": "128736676595", "true_name": "张亮", "cre_id": "230621199209193367"}
    # result = web.send_request(user_verify_url, 'verifyUserAuth', user_verify_parm)
    # bind_url = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
    # bind_parm = {"uid":"128736676617", # 已认证的uid
    #              "pay_pwd": "123456",  # 支付密码
    #              "mobile": "13274517393",  # 绑定的银行卡手机号
    #              "cre_id": "2306211992091933671",  # 身份证号
    #              "user_name": "张亮",  # 持卡人姓名
    #              "cardid": "b217991000022499904",  # 银行卡号
    #              "bank_type": "1001",  # 银行类型
    #              "bank_name": "邮政储蓄"
    #              }
    # bind_parm = {"uid":"128736676617", # 已认证的uid
    #              "pay_pwd": "123456",  # 支付密码
    #              "mobile": "13274517393",  # 绑定的银行卡手机号
    #              "cre_id": "230621199209193367",  # 身份证号
    #              "user_name": "张亮",  # 持卡人姓名
    #              "cardid": "6212263500015406958",  # 银行卡号
    #              "bank_type": "1001",  # 银行类型
    #              "bank_name": "中国银行"
    #              }
    # result = web.send_request(bind_url, 'bindBankCard', bind_parm)
    print(result)