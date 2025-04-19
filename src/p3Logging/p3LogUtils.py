# ---------------------------------------------------------------------------- +
"""
p3LogUtils.py - Utility functions for the p3Logging package.
These should be leaf level functions not dependent on any other p3l modules.
"""
# Standard Module Libraries
import logging
from pathlib import Path
from typing import Callable as function

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
#region force_exception() function
def force_exception(func, e:Exception=None) -> str:
    """ Force an exception to test exception handling. """
    func = force_exception if func is None else func
    dm = f"testcase: Default Exception Test for func:{func.__name__}()"
    e = ZeroDivisionError(dm) if e is None else e
    raise e
#endregion fpfx() function
# ---------------------------------------------------------------------------- +
