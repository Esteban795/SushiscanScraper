from errors import *
from functools import wraps
from typing import Callable
from logger import _getDebugLogger
from os.path import abspath
import inspect

CRITICAL = ["critical","fatal"]
NON_CRITICAL = ["error","warning","info","debug"]

def base_error_handler(func : Callable) -> Callable:
    """
    raises Error as explained below : 

    Expected : (in the form of Exception(msg,level))
    -> prints [time error level] message
    Example : 
    >>> raise ValueError('This is a value error.','warning') 
    would result in : ascii_time - expected - level - message

    Unexpected : (in the form of Exception(msg))
    -> logs ascii_time - expected - level - message
    Example :
    >>> raise ValueError('This is a value error.')
    would result in : ascii_time - unexpected - error - message being added to log_file
    """
    @wraps(func)
    def _wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except BaseException as e:
            _logError(e)
    return _wrapper

def _logError(error : BaseException) -> bool:
    tb = error.__traceback__
    lineno = tb.tb_lineno
    filename = abspath(inspect.getfile(tb))
    err_level = error.args[-1] if len(error.args) == 2 else None #check if we're on an expected error
    message = f"{filename} - {lineno} - {error.args[0]}"
    print(message)
    logger = _getDebugLogger(expected=True) if err_level else _getDebugLogger()
    if err_level in CRITICAL:
        logger.critical(message)
    elif err_level in NON_CRITICAL:
        logger.debug(message)
    else:
        logger.fatal(message)
    return True