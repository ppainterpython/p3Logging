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
#region t_of() function
def t_of(obj) -> str:
    return f"type({type(obj).__name__})"
#endregion t_of() function
# ---------------------------------------------------------------------------- +
#region v_of() function
def v_of(obj) -> str:
    return f"value = '{str(obj)}'"
#endregion v_of() function
# ---------------------------------------------------------------------------- +
#region check_testcase() function
def check_testcase(func, var : str, exc : str = "ZeroDivisionError") -> str:
    """ Raise test case exception exc if var = p3l.FORCE_EXCEPTION. 
    
    Used in functions and methods to enable test cases to force an exception
    to test exception handling.

    Args:
        func (function): The function calling for the check.
        var (str): The variable to be checked as equal to prl.FORCE_EXCEPTION.
        exc (str): The exception class name to be raised.

    Returns:
        str: A short string explaining why no exeption was raised.

    Raises:
        Exception: of the class name passed in the exc argument

    """
    # Validate input
    if var is None or not isinstance(var, str) or len(var.strip()) == 0:
        return F"param 'var' is not a non-empty string {v_of(var)}."
    if var != FORCE_EXCEPTION:
        return F"param 'var' is not equal to p3l.FORCE_EXCEPTION {v_of(var)}."
    if exc is None or not isinstance(var, str) or len(var.strip()) == 0:
        return F"param 'exc' is not a non-empty string {v_of(exc)}."
    func_valid = True if func is not None and isinstance(func, function) else False
    func_name = func.__name__ if func_valid else "unknownFunction"
    try:
        import builtins
        try:
            exc_class = getattr(builtins,exc)
            if exc_class is None or not isinstance(exc_class, type):
                return f"param 'exc' {v_of(exc)} is not a valid exception class name."
            dm = f"testcase: {exc} Exception Test for func:{func_name}()"
            te = exc_class(dm)
            raise te
        except AttributeError as e:
            return f"param 'exc' {v_of(exc)} error retrieving from builtins: str{e}."
    except Exception as e:
        if e == te:
            raise e
        return f"Error creating {exc}(), msg = '{str(e)}'"
#endregion check_testcase() function
# ---------------------------------------------------------------------------- +
