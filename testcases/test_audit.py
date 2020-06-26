from middlerware.handler import Handler, MySqlHandlerWare, replace_data
from common.requset_handler import visit
import ddt
import unittest
import json

# 读取审核用例
audit_data = Handler.excel.read_sheet("审核")

# 初始化logger
logger = Handler.logger


@ddt.ddt
class TestAudit(unittest.TestCase):

    @ddt.data(*audit_data)
    def test_audit(self, test_info):

        test_info["headers"] = replace_data(Handler(), test_info["headers"])

        test_info["data"] = replace_data(Handler(), test_info["data"])

        resp = visit(method=test_info["method"],
                     url=Handler.host + test_info["url"],
                     json=json.loads(test_info["data"]),
                     headers=eval(test_info["headers"]))
        expected = eval(test_info["expected"])
        self.assertTrue(expected["code"] == resp["code"])
        self.assertTrue(expected["msg"] == resp["msg"])

        if resp["code"] == 0:
            # 验证数据库状态
            data = json.loads(test_info["data"])
            loan = MySqlHandlerWare().query("SELECT * FROM loan WHERE id={}".format(data["loan_id"]))
            self.assertEqual(expected["status"], loan["status"])

        logger.info("第{}条测试用例通过".format(test_info["case_id"]))

