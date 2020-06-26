import logging
import requests


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

if __name__ == '__main__':
    pass
