"""
------------------------------------
@Time : 2019/6/18 9:28
@Auth : linux超
@File : SendEmail.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import yagmail

from common.RecordLog import logger


class SendMailWithReport(object):
    """发送邮件"""

    logger.info("开始发送邮件报告")

    @staticmethod
    def send_mail(smtp_server, from_user, from_pass_word, to_user, subject, contents, file_name):
        # 初始化服务器等信息
        try:
            yag = yagmail.SMTP(from_user, from_pass_word, smtp_server)
            # 发送邮件
            yag.send(to_user, subject, contents, file_name)
        except Exception as e:
            logger.error("发送邮件失败!\n失败信息:{}".format(e))
        else:
            logger.info("发送{}邮件成功".format(file_name))


if __name__ == '__main__':
    SendMailWithReport.send_mail('smtp.qq.com',
                                 '281754043@qq.com',
                                 'ywjqtmrwqfuqbhdi',
                                 '281754043@qq.com',
                                 'python自动化测试',
                                 '邮件正文',
                                 '17_12_07.html')
