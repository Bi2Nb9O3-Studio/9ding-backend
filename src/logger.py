import logging
from math import log
import time

logfile = "./logs/"+time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())+".log"
print(logfile)

def get_logger(name):
    global logfile
    print("get logger")
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger=setlogger(logger)
    return logger

def setlogger(logger):
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    fh = logging.FileHandler(logfile)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
