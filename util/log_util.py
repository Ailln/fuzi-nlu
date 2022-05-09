import time
import pathlib
import logging


def get_logger(name: str = "fuz-nlu", level: str = "info") -> logging.Logger:
    logger = logging.getLogger(name)
    level_dict = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }
    logger.setLevel(level_dict[level])

    if not logger.handlers:
        log_path = log_path_util()
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)
        fh_fmt = logging.Formatter("%(asctime)-15s [%(filename)s] %(levelname)s %(lineno)d: %(message)s")
        fh.setFormatter(fh_fmt)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console_fmt = logging.Formatter("%(asctime)-15s [%(filename)s] %(levelname)s %(lineno)d: %(message)s")
        console.setFormatter(console_fmt)

        logger.addHandler(fh)
        logger.addHandler(console)

    return logger


def log_path_util(name: str = "fuzi-nlu") -> str:
    day = time.strftime("%Y-%m-%d", time.localtime())
    log_path = pathlib.Path(f"./log/{day}")
    if not log_path.exists():
        log_path.mkdir(parents=True)
    return f"{str(log_path)}/{name}.log"
