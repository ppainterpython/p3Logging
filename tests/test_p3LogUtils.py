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
        result = p3l.fpfx(p3l.force_exception(p3l.fpfx))
    assert f"InvalidFunction({p3l.force_exception}): ", \
        f"Expected {result} to be InvalidFunction({p3l.force_exception}): "
#endregion test_fpfx() function
# #endregion Tests for fpfx() function
# ---------------------------------------------------------------------------- +