import os
import unittest
from datetime import datetime
from common.email_hander import SendMailWithReport
from config import config
from library.HTMLTestRunnerNew import HTMLTestRunner
from middlerware.handler import Handler

# 加载测试用例
loader = unittest.TestLoader()

# 加载所有的测试用例
cases_suit = loader.discover(config.CASE_PATH)
report_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report_file = os.path.join(config.REPORT_PATH, "TestReport"+report_name+".html")
# 获取HTML测试报告
if __name__ == '__main__':
    with open(report_file, "wb") as f:
        runner = HTMLTestRunner(f, title="python自动化测试报告", description="测试详情", tester="小汪")
        runner.run(cases_suit)
    SendMailWithReport.send_mail(**Handler.yaml_data["email_address"], file_name=report_file)
    print("邮件发送成功")
