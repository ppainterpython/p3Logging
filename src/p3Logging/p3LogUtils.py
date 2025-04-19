# ---------------------------------------------------------------------------- +
"""
p3LogUtils.py - Utility functions for the p3Logging package.
These should be leaf level functions not dependent on any other p3l modules.
"""
# Standard Module Libraries
import logging
from typing import Callable as function
from pathlib import Path

# Local Modules
from .p3LogConstants import *  

# ---------------------------------------------------------------------------- +
#region is_filename_only() function
def is_filename_only(path_str: str = None) -> bool:
    """ Check path_str as name of file only, no parent. """
    # Validate input
    if path_str is None or not isinstance(path_str, str) or len(path_str.strip()) == 0:
        raise TypeError(f"Invalid path_str: type='{type(path_str).__name__}', value='{path_str}'")
    
    path = Path(path_str)
    # Check if the path has no parent folders    
    return path.parent == Path('.')
#endregion is_filename_only() function
# ---------------------------------------------------------------------------- +
#region append_cause() function
def append_cause(msg:str = None, e:Exception=None, depth:int=0) -> str:
    """ Append the cause chain of an exception to the message. """
    # If the exception has a cause, append the chain up to depth
    exc = e
    msg = ""
    t1 = t2 = True
    while t1 or t2:
        msg += f"Exception({depth}): {str(exc)}"
        msg += f" >>> " if depth > 0 else ""
        t1 = exc.__cause__ is not None and exc != exc.__cause__ 
        t2 = exc.__context__ is not None and exc != exc.__context__
        exc = exc.__cause__ or exc.__context__
        depth -= 1 if depth > 0 else 0
    return msg 
#endregion append_cause() function
# ---------------------------------------------------------------------------- +
#region fpfx() function
def fpfx(func) -> str:
    """
    Return a prefix for the function name and its module.
    """
    try:
        if func is not None and isinstance(func, function):
            mod_name = func.__globals__['__name__']
            func_name = func.__name__
            # Helpling out the test cases only.
            if func_name == "force_exception":
                force_exception(func)
            return f"{mod_name}.{func_name}(): "
        else: 
            m = f"InvalidFunction({str(func)}): "
            print(f"fpfx(): Passed {str(m)}")
            return m
    except Exception as e:
        print(f"fpfx() Error: {str(e)}")
        raise
#endregion fpfx() function
# ---------------------------------------------------------------------------- +
#region exc_msg() function
def exc_msg(func:function,e:Exception,
            print_flag:bool=False) -> str:
    """
    Common simple output message for Exceptions.
    
    Within a function, use to emit a message in except: blocks. Various 
    arguments select output by console print(), logger, or both.
    
    Args:
        func (function): The function where the exception occurred.
        e (Exception): The exception object.
        print (bool): If True, print the message to console.
        log (logging.Logger): Logger object to log the message.
        
    Returns:
        str: Returns the routine exception log message.    
    """
    try:
        if func is not None and isinstance(func, function):
            # Helpling out the test cases only.
            if func.__name__ == "force_exception":
                force_exception(func)
            m = f"{fpfx(func)}{str(e)}"
            if print_flag: print(m)
            return m
        else:
            m = f"exc_msg(): Invalid func param:'{str(func)}'"
            if print_flag: print(m)
            return m
    except Exception as e:
        print(f"p3LogUtils.exc_msg() Error: {str(e)}")
        raise
#endregion exc_msg() function
# ---------------------------------------------------------------------------- +
#region force_exception() function
def force_exception(func, e:Exception=None) -> str:
    """ Force an exception to test exception handling. """
    func = force_exception if func is None else func
    dm = f"testcase: Default Exception Test for func:{func.__name__}()"
    e = ZeroDivisionError(dm) if e is None else e
    raise e
#endregion fpfx() function
# ---------------------------------------------------------------------------- +
