import logging
import requests


# 不带cookies
def visit(method, url, params=None, data=None, json=None, **kwargs):
    try:
        res = requests.request(method=method,
                               url=url,
                               params=params,
                               data=data,
                               json=json,
                               **kwargs)
        return res.json()
    except ValueError as e:
        logging.error(f"返回的不是json格式:{e}")


# 带cookies
def visit1(method, url, params=None, data=None, json=None, **kwargs):
    try:
        session = requests.session()
        res = session.request(method=method,
                              url=url,
                              params=params,
                              data=data,
                              json=json,
                              **kwargs)
        return res.json()
    except ValueError as e:
        logging.error(f"返回的不是json格式:{e}")

if __name__ == '__main__':
    pass
