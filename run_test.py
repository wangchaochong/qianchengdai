import os
import unittest
from datetime import datetime
from library.HTMLTestRunnerNew import HTMLTestRunner
from config import config
from middlerware.handler import Handler
from common.email_hander import SendMailWithReport

# 加载测试用例
loader = unittest.TestLoader()

# 加载所有的测试用例
cases_suit = loader.discover(config.CASE_PATH)
# report_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report_file = os.path.join(config.REPORT_PATH, "前程贷接口测试报告.html")
# 获取HTML测试报告
if __name__ == '__main__':
    with open(report_file, "wb") as f:
        runner = HTMLTestRunner(f, title="python自动化测试报告", description="测试详情", tester="小汪")
        runner.run(cases_suit)
        # SendMailWithReport.send_mail(**Handler.yaml_data["email_address"], file_name=report_file)
        # print("邮件发送成功")
