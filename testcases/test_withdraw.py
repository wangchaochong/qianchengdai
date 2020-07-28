import json
import unittest
from decimal import Decimal
from common.requset_handler import visit
from middlerware.handler import Handler, MySqlHandlerWare
import ddt

# 初始化logger
logger = Handler.logger
# 获取提现记录
withdraw_data = Handler.excel.read_sheet("提现")


@ddt.ddt
class TestWithdraw(unittest.TestCase):
    # 下面的方法只执行一次
    @classmethod
    def setUpClass(cls):
        cls.token = Handler().token
        cls.member_id = Handler().member_id
        cls.other_member_id = Handler().other_member_id
        cls.db = MySqlHandlerWare()
        sql = "SELECT leave_amount FROM member WHERE id = {};".format(cls.member_id)
        leave_amount_dict = cls.db.query(sql)
        leave_money = leave_amount_dict["leave_amount"]
        if leave_money < 501999.22 or leave_money >= 503500.22:
            cls.db.update("UPDATE member SET leave_amount = 501999.22 WHERE id = {};".format(cls.member_id))

        if leave_money < 1000:
            cls.db.update("UPDATE member SET leave_amount = 501999.22 WHERE id = {};".format(cls.other_member_id))

    # 前置条件、
    def setUp(self):
        self.db = MySqlHandlerWare()

    def tearDown(self):
        self.db.close()

    @ddt.data(*withdraw_data)
    def test_withdraw(self, test_info):
        if "#token#" in test_info["headers"]:
            test_info["headers"] = test_info["headers"].replace("#token#", self.token)

        if "#member_id#" in test_info["data"]:
            test_info["data"] = test_info["data"].replace("#member_id#", str(self.member_id))

        if "#other_member_id#" in test_info["data"]:
            test_info["data"] = test_info["data"].replace("#other_member_id#", str(self.other_member_id))

        url = Handler.host + test_info["url"]
        sql = "select * from member where id = {};".format(self.member_id)
        before_data = self.db.query(sql)
        before_money = before_data["leave_amount"]

        resp = visit(method=test_info["method"],
                     url=url,
                     json=eval(test_info["data"]),
                     headers=json.loads(test_info["headers"]))
        try:
            for key, value in eval(test_info["expected"]).items():
                self.assertTrue(resp[key] == value)
            if resp["code"] == 0:
                # 查询之后的余额
                sql = "select * from member where id = {};".format(self.member_id)
                after_data = self.db.query(sql)
                after_money = after_data["leave_amount"]
                data = json.loads(test_info["data"])["amount"]
                new_money = before_money - Decimal(str(data))
                # print(new_money)
                self.assertTrue(new_money == after_money)
            logger.info("第{}条测试用例通过".format(test_info["case_id"]))
        except Exception as e:
            raise e

if __name__ == '__main__':
    unittest.main()
