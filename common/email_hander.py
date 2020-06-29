import yagmail


class SendMailWithReport(object):
    """发送邮件"""

    @staticmethod
    def send_mail(smtp_server, from_user, from_pass_word, to_user, subject, contents, file_name=None):
        """

        :param smtp_server: 邮箱提供商的服务地址
        :param from_user: 发件人
        :param from_pass_word: 发件人的密码（不一定是登录密码， 如 qq 邮箱就是授权码）
        :param to_user: 收件人，支持多人，列表格式
        :param subject: 主题
        :param contents: 正文
        :param file_name: 附件
        :return:
        """
        # 初始化服务器等信息
        yag = yagmail.SMTP(from_user, from_pass_word, smtp_server)
        # 发送邮件
        yag.send(to_user, subject, contents, file_name)



if __name__ == '__main__':
    SendMailWithReport.send_mail('smtp.qq.com',
                                 '****@qq.com',
                                 'password',
                                 ['***@qq.com', '***@qq.com'],
                                 'python自动化测试',
                                 '邮件正文',
                                 './result.xlsx')
