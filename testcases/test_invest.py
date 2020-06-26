import json
import unittest, ddt
from decimal import Decimal
from middlerware.handler import Handler, replace_data, MySqlHandlerWare
from common.requset_handler import visit
# 获取投资测试用例
invest_data = Handler.excel.read_sheet("投资")

# 初始化logger
logger = Handler.logger

@ddt.ddt
class TestInvest(unittest.TestCase):
    def setUp(self):
        self.db = MySqlHandlerWare()

    def tearDown(self):
        self.db.close()

    @ddt.data(*invest_data)
    def test_invest(self, test_info):

        test_info["data"] = replace_data(Handler(), test_info["data"])
        test_info["headers"] = replace_data(Handler(), test_info["headers"])
        # 访问之前查数据库
        check_sql = test_info["check_sql"]

        if check_sql == 1:
            now_member_id = eval(test_info["data"])["member_id"]
            before_money_d = self.db.query("SELECT * FROM member WHERE id = {};".format(now_member_id))
            before_data = self.db.query("SELECT ID FROM financelog;", one=False)

        resp = visit(method=test_info["method"],
                     url=Handler.host + test_info["url"],
                     json=json.loads(test_info["data"]),
                     headers=json.loads(test_info["headers"]))

        expected = json.loads(test_info["expected"])
        self.assertTrue(expected["code"] == resp["code"])
        self.assertTrue(expected["msg"] == resp["msg"])
        if resp["code"] == 0:
            # 会生成一条投资id
            invest_id = resp["data"]["id"]

            # 查询数据库看有没有生成此记录
            invest_dd = self.db.query("SELECT * FROM invest WHERE id = {};".format(invest_id))
            self.assertTrue(invest_dd)
            # financelog表增加一条记录
            after_data = self.db.query("SELECT ID FROM financelog;", one=False)
            self.assertTrue(len(before_data) + 1 == len(after_data))

            # 投资余额减少
            after_money_d = self.db.query("SELECT * FROM member WHERE id = {};".format(now_member_id))
            invest_momey = resp["data"]["amount"]
            before_money = before_money_d["leave_amount"]
            after_money = after_money_d["leave_amount"]
            invest_momey = Decimal(str(invest_momey))
            self.assertTrue(before_money - invest_momey == after_money)
            logger.info("第{}条测试用例通过".format(test_info["case_id"]))

if __name__ == '__main__':
    unittest.main()
