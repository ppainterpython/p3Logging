# ---------------------------------------------------------------------------- +
# test_p3LogUtils.py
# ---------------------------------------------------------------------------- +
#region imports
# python standard libraries
import logging, pytest, os
from pathlib import Path

# third-party libraries
import inspect, pyjson5

# local libraries
import p3Logging as p3l
#endregion imports
# ---------------------------------------------------------------------------- +
#region Globals
THIS_APP_NAME = "Test_p3Config"

root_logger = logging.getLogger()
logger = logging.getLogger(THIS_APP_NAME)
logger.propagate = True
#endregion Globals
# ---------------------------------------------------------------------------- +
#region Tests for is_filename_only() function
# ---------------------------------------------------------------------------- +
#region test_is_filename_only() function
def test_is_filename_only():
    # Test with a valid filename
    result = p3l.is_filename_only("test_file.txt")
    assert result is True, f"Expected True but got {result}"

    # Test with a path that has parent directories
    result = p3l.is_filename_only("/path/to/test_file.txt")
    assert result is False, f"Expected False but got {result}"

    # Test with an empty string
    with pytest.raises(TypeError) as excinfo:
        result = p3l.is_filename_only("")
    assert str(excinfo.value) == "Invalid path_str: type='str', value=''", \
     f"Expected TypeError but got {str(excinfo.value)}"

    # Test with None
    with pytest.raises(TypeError) as excinfo:   
        result = p3l.is_filename_only(None)
    assert str(excinfo.value) == "Invalid path_str: type='NoneType', value='None'", \
        f"Expected TypeError but got {str(excinfo.value)}"
#endregion test_is_filename_only() function
# ---------------------------------------------------------------------------- +
#endregion Tests for is_filename_only() function
# ---------------------------------------------------------------------------- +
#region Tests for fpfx() function
# ---------------------------------------------------------------------------- +
#region test_fpfx() function
def test_fpfx():
    # Test with a valid function
    def test_func():
        pass

    result = p3l.fpfx(test_func)
    assert result == f"{test_func.__module__}.{test_func.__name__}(): ", f"Expected {result} to be {test_func.__module__}.{test_func.__name__}(): "

    # Test with an invalid function
    result = p3l.fpfx(None)
    assert result == f"InvalidFunction(None): ", \
        f"Expected {result} to be InvalidFunction(None): "
    # Test with forced exception
    e = ZeroDivisionError("testcase: test_fpfx()")
    with pytest.raises(ZeroDivisionError) as excinfo:
        result = p3l.fpfx(p3l.force_exception)
    exp_msg = f"testcase: Default Exception Test for func:force_exception()"
    assert exp_msg in str(excinfo.value), \
        f"Expected Exception msg to be '{exp_msg}' but got '{str(excinfo.value)}'"
#endregion test_fpfx() function
# ---------------------------------------------------------------------------- +
#endregion Tests for fpfx() function
# ---------------------------------------------------------------------------- +
#region Tests for append_cause() function
# ---------------------------------------------------------------------------- +
#region test_append_cause() function
def test_append_cause():
    # Test with a chain of valid exceptions
    depth = 4
    def recurse_exception_func(depth:int = 4, e:Exception = None):
        try:
            ee = TypeError(f"TypeError: Func-{depth}:")
            ee = ValueError(f"ValueError: Func-{depth}:") if depth % 2 else ee
            if depth == 0:
                raise ee # base level, stops recursion
            else:
                recurse_exception_func(depth - 1, ee)
        except Exception as e:
            raise ee from e # chains exceptions back up the stack
    try:
        recurse_exception_func(depth)
    except Exception as e:
        result = p3l.append_cause("test_append_cause():", e, depth)
        em = "TypeError: Func-4: >>> "
        assert em in result, f"Expected '{em}' in {result}"
        em = "ValueError: Func-3: >>> "
        assert em in result, f"Expected '{em}' in {result}"

#endregion test_append_cause() function
#endregion Tests for append_cause() function
# ---------------------------------------------------------------------------- +
