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
def is_filename_only(path_str:str = None) -> bool:
    """
    Check path_str as name of file only, no parent.
    """
    path = Path(path_str)
    # Check if the path has no parent folders    
    return path.parent == Path('.')
#endregion is_filename_only() function
# ---------------------------------------------------------------------------- +
#region append_cause() function
def append_cause(msg:str = None, e:Exception=None) -> str:
    """
    Append the cause of an exception to the message.
    """
    # If the exception has a cause, append it to the message
    print(f"{str(e)} - > {str(e.__cause__)}")
    if e:
        if e.__cause__:
            msg += append_cause(f" Exception: {str(e)}",e.__cause__) 
        else:
            msg += f" Exception: {str(e)}"
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
        if not func is None and isinstance(func, function):
            m = f"{fpfx(func)}{str(e)}"
            if print_flag: print(m)
            return m
        else:
            m = f"exc_msg(): InvalidF func param:'{str(func)}'"
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
