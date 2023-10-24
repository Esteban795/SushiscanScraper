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
            if isinstance(e,KeyboardInterrupt):
                exit(1)
            _logError(e)
    return _wrapper

def try_until_no_error(func : Callable) -> Callable:
    """
    Attemps to call the function until no error is raised.
    """
    def wrapper(*args,**kwargs):
        while True:
            try:
                return func(*args,**kwargs)
            except BaseException as e:
                if isinstance(e,KeyboardInterrupt):
                    exit(0)
                else:
                    _logError(e)
    return wrapper

def back_to_main_loop(func : Callable) -> Callable:
    def wrapper(self):
        try:
            func(self)
        except BaseException as e:
            if isinstance(e,KeyboardInterrupt):
                exit(0)
            else:
                _logError(e)
                self.loop()
    return wrapper

def _logError(error : BaseException) -> bool:
    tb = error.__traceback__
    lineno = tb.tb_lineno
    filename = abspath(inspect.getfile(tb))
    err_level = error.args[-1] if len(error.args) == 2 else None #check if we're on an expected error
    message = f"{filename} - {lineno} - {error.args[0]}"
    logger = _getDebugLogger(expected=True) if err_level else _getDebugLogger()
    if err_level in CRITICAL:
        logger.critical(message)
    elif err_level in NON_CRITICAL:
        logger.debug(message)
    else:
        logger.fatal(message)
    return True