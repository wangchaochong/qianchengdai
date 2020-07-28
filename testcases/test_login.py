import json
import random
import unittest
import ddt
from common.requset_handler import visit
from middlerware.handler import Handler, MySqlHandlerWare

# 初始化logger
logger = Handler.logger

# 读取登录Excel表格
login_data = Handler.excel.read_sheet("登录")
logger.info("已读取表格文件")


@ddt.ddt
class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.phone = TestLogin().random_phone()
        cls.phone_yes = TestLogin().phone_yes()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @ddt.data(*login_data)
    def test_login(self, test_info):
        # phone = self.random_phone()
        # phone_yes = self.phone_yes()
        if "#phone#" in test_info["data"]:
            test_info["data"] = test_info["data"].replace("#phone#", self.phone)
        if "#yes_phone#" in test_info["data"]:
            test_info["data"] = test_info["data"].replace("#yes_phone#", self.phone_yes)

        data = json.loads(test_info["data"])
        url = Handler().host + test_info["url"]
        resp = visit(test_info["method"],
                     url=url,
                     json=json.loads(test_info["data"]),
                     headers=json.loads(test_info["headers"]))
        try:
            for k, v in json.loads(test_info["expected"]).items():
                self.assertEqual(resp[k], v)
            if resp[k] == 0:
                db_data = MySqlHandlerWare().query("select * from member where mobile_phone = {};".format(data["mobile_phone"]))
                self.assertTrue(db_data)
            Handler.excel.write("登录", test_info["case_id"] + 1, 9, "通过")
            logger.info("第{}条测试用例通过".format(test_info["case_id"]))
        except Exception as e:
            logger.info("第{}条测试用例失败".format(test_info["case_id"]))
            print(f"返回的不是jsong格式：{e}")
            Handler.excel.write("登录", test_info["case_id"] + 1, 9, "失败")
            raise e

    # 生成没注册的手机号
    def random_phone(self):
        while True:
            end_num = "".join(random.sample(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 8))
            phone_number = "158" + end_num
            phone_data = MySqlHandlerWare().query("select * from member where mobile_phone = {};".format(phone_number))
            if not phone_data:
                # db_con.close()
                return phone_number
            MySqlHandlerWare().close()

    # 已经注册的手机号
    def phone_yes(self):
        phone_data = MySqlHandlerWare().query("select mobile_phone from member;")
        return phone_data["mobile_phone"]

if __name__ == '__main__':
    unittest.main()


