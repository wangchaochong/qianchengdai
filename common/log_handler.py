import logging


def get_logging(name="root",
                logger_lev="DEBUG",
                file_name=None,
                stream_lev="DEBUG",
                file_lev="INFO",
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(filename)s[line:%(lineno)d] - %(message)s"
                ):
    # 初始化收集器
    logger = logging.getLogger(name)
    # 设置收集器级别
    logger.setLevel(logger_lev)
    # 初始化处理器
    if file_name:
        file_handler = logging.FileHandler(file_name, encoding="utf-8")
        # 设置级别
        file_handler.setLevel(file_lev)
        # 设置输出格式
        format_1 = logging.Formatter(fmt)
        file_handler.setFormatter(format_1)
        logger.addHandler(file_handler)

    # 控制台输出
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(stream_lev)
    # 设置输出格式
    fmt = logging.Formatter(fmt)
    stream_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)

    return logger


if __name__ == '__main__':
    logger = get_logging()
    logger.info(888)
