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
from common.RecordLog import logger


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
                logger.info('获得请求参数<{}>'.format(data))
            except Exception:
                try:
                    data = eval(data)
                    logger.info('获得请求参数<{}>'.format(data))
                except Exception as e:
                    logger.error("获得请求参数失败\n错误详情:{}".format(e))
                    raise e
        service = WebService.get_client_obj(url)
        my_api = getattr(service, api)
        try:
            logger.info("开始发送[{}]请求".format(api))
            response = my_api(data)
        except WebFault as e:
            response = e.fault
            logger.info("返回[{}]接口响应信息为:\n{}".format(api, response))
            return response
        else:
            logger.info("返回[{}]接口响应信息为:\n{}".format(api, response))
            return response

    def __call__(self, url, api, data):
        response = self.send_request(url=url, api=api, data=data)
        return response


if __name__ == '__main__':
    web = WebService()
    send_code_url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'
    send_parm = '{"client_ip": "192.168.1.1", "tmpl_id": [1], "mobile": "13425356846"}'
    result = web(send_code_url, 'sendMCode', send_parm)
    print(result)
