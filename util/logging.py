from datetime import datetime
from time import gmtime, strftime

# todo: formatting n stuff
from enum import Enum
import os


brackets: str = '[]'
log_dir: str = "_logs"
log_extension: str = ".log"
time_fmt: str = "%Y-%m-%d"


class LogLevel(Enum):
    DEBUG = 0,
    INFO = 1,
    WARN = 2,
    ERROR = 3


async def log(message: str, log_level: LogLevel = LogLevel.INFO):
    # set up the log message, including timezone
    timezone: str = strftime("%Z", gmtime())
    log_message: str = f"{brackets[0]}{log_level.name}{brackets[1]} {brackets[0]}{datetime.now()} {timezone}{brackets[1]} : {message}"
    # ensure the logs directory exists
    logdir: str = get_log_directory()
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    # now open the file, write to it, and close it
    log_file = None
    filename = get_log_filename()
    log_file = open(filename, "a+")
    if log_file is None:
        print("Error: unable to open log file " + filename + ".")
        return
    print(log_message, file=log_file)
    log_file.close()
    # also print to stdout
    print(log_message)


def get_log_filename() -> str:
    return os.path.join(get_log_directory(), datetime.now().strftime(time_fmt) + log_extension)


def get_log_directory() -> str:
    return os.path.join(os.getcwd(), log_dir)
