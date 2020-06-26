import json
import random
import unittest
import ddt
from common.requset_handler import visit
from middlerware.handler import Handler, MySqlHandlerWare

# 实例化logger日志对象
logger = Handler.logger

# 通过yaml获取Excel表格数据
register_data = Handler.excel.read_sheet("注册")
logger.info("我正在获取Excel数据")


# 随机获取手机号
def random_phone():
    while True:
        end_num = "".join(random.sample(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 8))
        phone_number = "158" + end_num
        phone_data = MySqlHandlerWare().query("select * from member where mobile_phone = {};"
                                              .format(phone_number))
        if not phone_data:
            MySqlHandlerWare().close()
            return phone_number
        MySqlHandlerWare().close()


@ddt.ddt
class TestRegister(unittest.TestCase):
    # 前置条件，只执行一次
    @classmethod
    def setUpClass(cls):
        cls.phone = random_phone()

    @ddt.data(*register_data)
    def test_register(self, test_info):
        if "#phone#" in test_info["data"]:
            test_info["data"] = (test_info["data"]).replace("#phone#", self.phone)

        data = json.loads(test_info["data"])
        url = Handler().host + test_info["url"]
        resp = visit(test_info["method"],
                     url,
                     json=json.loads(test_info["data"]),
                     headers=json.loads(test_info["headers"]))
        try:
            for key, value in json.loads(test_info["expected"]).items():
                self.assertEqual(resp[key], value)
            if resp["code"] == 0:
                sql = "select * from member where mobile_phone = {};".format(data["mobile_phone"])
                phone_data = MySqlHandlerWare().query(sql)
                self.assertTrue(phone_data)
            logger.info("第{}条测试用例通过".format(test_info["case_id"]))

        except Exception as e:
            print(f"返回的数据不是json格式:{e}")
            raise e

if __name__ == '__main__':
    unittest.main()




