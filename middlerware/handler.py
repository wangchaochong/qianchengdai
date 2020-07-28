import json
import os
# from common.email_hander import send_mail
import re
from jsonpath import jsonpath
from pymysql.cursors import DictCursor
from common.requset_handler import visit
from common.excel_handler import ExcelHandler
from common.mysql_handler import MysqlHandler
from common.yaml_handler import red_config
from config import config
from common.log_handler import get_logging


class Handler():
    # 环境地址
    host = "http://120.78.128.25:8766/"

    # 获取yaml文件内容
    yaml_data = red_config(config.CONF_PATH)
    # 初始化logger
    logger = get_logging(**yaml_data["log"], file_name=config.LOG_PATH)
    # 读取Excel表格
    excel = ExcelHandler(os.path.join(config.DATA_PATH, yaml_data["excel"]["file_name"]))

    # 发送邮件
    # send_mail = send_mail(**yaml_data["email_address"], file_name="")

    @property
    def token(self):
        return login(Handler.yaml_data["user"])["token"]

    @property
    def other_token(self):
        return login(Handler.yaml_data["other_user"])["token"]

    @property
    def member_id(self):
        return login(Handler.yaml_data["user"])["member_id"]

    @property
    def other_member_id(self):
        return login(Handler.yaml_data["other_user"])["member_id"]

    @property
    def admin_token(self):
        return login(Handler.yaml_data["admin_user"])["token"]

    @property
    def loan_id(self):
        return loan_id()

    @property
    def loan_id_pass(self):
        return loan_id_pass()

    @property
    def audit_loan_id(self):
        return audit_loan_id()


class MySqlHandlerWare(MysqlHandler):
    """
    继承MysqlHandler,
    """
    def __init__(self):
        """
        初始化所有的配置项，从yaml中读取
        """
        db_config = Handler().yaml_data["db"]
        super().__init__(host=db_config["host"],
                         port=3306,
                         user=db_config["user"],
                         password=db_config["password"],
                         charset="UTF8",
                         database=db_config["database"],
                         cursorclass=DictCursor)


def login(user):
    url = Handler.host + "futureloan/member/login"
    data = user
    headers = {"X-Lemonban-Media-Type": "lemonban.v2", "Content-Type": "application/json"}
    res = visit(url=url,
                method="post",
                json=data,
                headers=headers)
    token_1 = jsonpath(res, "$..token")[0]
    token_type = jsonpath(res, "$..token_type")[0]
    token = " ".join((token_type, token_1))
    member_id = jsonpath(res, "$..id")[0]
    return {"token": token, "member_id": member_id}


def loan_id():
    item_data = {"member_id": Handler().member_id,
                 "title": "买车",
                 "amount": 50000,
                 "loan_rate": 20.0,
                 "loan_term": 30,
                 "loan_date_type": 2,
                 "bidding_days": 10}
    headers = {"X-Lemonban-Media-Type": "lemonban.v2",
               "Content-Type": "application/json",
               "Authorization": Handler().token}
    resp = visit(method="post",
                 url=Handler.host + "futureloan/loan/add",
                 json=item_data,
                 headers=headers)
    return jsonpath(resp, "$..id")[0]


def audit_loan_id():
    headers = {"X-Lemonban-Media-Type": "lemonban.v2",
               "Content-Type": "application/json",
               "Authorization": Handler().admin_token}
    data = {"loan_id": Handler().loan_id, "approved_or_not": True}
    visit(method="patch", url=Handler.host + "futureloan/loan/audit", json=data, headers=headers)
    return data["loan_id"]


def loan_id_pass():
    # 查数据库
    db = MySqlHandlerWare()
    data = db.query("SELECT * FROM loan WHERE status != 1;")
    return data["id"]


# 难点
def replace_data(object, data):
    patten = r"#(.*?)#"
    while re.search(patten, data):
        key = re.search(patten, data).group(1)
        value = getattr(object, key, "")
        data = re.sub(patten, str(value), data, 1)
    return data


if __name__ == '__main__':
    # print(Handler.send_mail)
    print(Handler().admin_)

    # print(audit_loan_id())




