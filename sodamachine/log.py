import logging
from settings import DAEMON_LOG_PATH, SYSTEM_LOG_PATH, TRANSACTION_LOG_PATH

def createSystemLogger():
    sysLogger = logging.getLogger(__name__)
    sysLogger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler(SYSTEM_LOG_PATH)
    fileHandler.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S')

    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)

    sysLogger.addHandler(fileHandler)
    sysLogger.addHandler(consoleHandler)

    return(sysLogger)

def createTransactionLogger():
    transLogger = logging.getLogger(__name__)
    transLogger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler(TRANSACTION_LOG_PATH)
    fileHandler.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S')

    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)

    transLogger.addHandler(fileHandler)
    transLogger.addHandler(consoleHandler)
    transLogger.info("--------------------------------------------------------")
    transLogger.info("[START] Beginning transaction for a user")

    return(transLogger)
