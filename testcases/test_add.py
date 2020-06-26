import unittest
import ddt
import json
from middlerware.handler import Handler, MySqlHandlerWare, replace_data
from common.requset_handler import visit


logger = Handler.logger

add_data = Handler.excel.read_sheet("新增项目")


@ddt.ddt
class TestAdd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.member_id = Handler().member_id

    def setUp(self):
        self.db = MySqlHandlerWare()
        sql = "select * from loan where member_id = {}".format(self.member_id)
        self.before_loan = self.db.query(sql, one=False)

    def tearDown(self):
        self.db.close()

    @ddt.data(*add_data)
    def test_add_item(self, test_info):
        url = Handler.host + test_info["url"]
        test_info["data"] = replace_data(Handler(), test_info["data"])
        test_info["headers"] = replace_data(Handler(), test_info["headers"])
        resp = visit(method=test_info["method"],
                     url=url,
                     json=json.loads(test_info["data"]),
                     headers=json.loads(test_info["headers"]))
        try:
            expected = json.loads(test_info["expected"])
            self.assertTrue(expected["code"] == resp["code"])
            self.assertTrue(expected["msg"] == resp["msg"])

            if resp["code"] == 0:
                sql = "select * from loan where member_id = {}".format(self.member_id)
                after_loan = self.db.query(sql, one=False)
                self.assertTrue(len(self.before_loan) + 1 == len(after_loan))
            logger.info("第{}条测试用例通过".format(test_info["case_id"]))

        except Exception as e:
            logger.error("请求不是json格式")
            raise e


if __name__ == '__main__':
    unittest.main()
