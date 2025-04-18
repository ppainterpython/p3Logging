# ---------------------------------------------------------------------------- +
# test_p3LogConfig.py
# ---------------------------------------------------------------------------- +
#region imports
# python standard libraries
import logging, pytest

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
#region Tests for p3LogConfig.setup_logging() function
# ---------------------------------------------------------------------------- +
#region test_setup_logging_with_FileHandler_filenames_input() function
def test_setup_logging_with_FileHandler_filenames_input():
    # Initialize the logger from a logging configuration file.
    filenames = {"file": "logs/p3Logging-file-test.log", 
                 "json_file": "logs/p3Logging-json_file-test.log"}
    config_file: str = p3l.STDOUT_FILE_LOG_CONFIG_FILE
    assert p3l.quick_logging_test(THIS_APP_NAME, config_file,filenames), \
        f"Expected quick_logging_test({config_file}) to return True"
    config_file: str = p3l.STDERR_FILE_JSON_LOG_CONFIG_FILE
    assert p3l.quick_logging_test(THIS_APP_NAME, config_file,filenames), \
        f"Expected quick_logging_test({config_file}) to return True"
#endregion test_setup_logging_with_FileHandler_filenames_input() function
# ---------------------------------------------------------------------------- +
#endregion Tests for p3LogConfig.setup_logging() function
# ---------------------------------------------------------------------------- +
#region Tests for quick_logging_test() function
# ---------------------------------------------------------------------------- +
#region test_quick_logging_test_builtin_config_cases() function
_BUILTIN_CONFIG_TEST_CASES = [
    (p3l.STDOUT_LOG_CONFIG_FILE, True),
    (p3l.STDOUT_FILE_LOG_CONFIG_FILE, True),
    (p3l.STDERR_FILE_JSON_LOG_CONFIG_FILE, True),
    (p3l.QUEUED_STDERR_FILE_JSON_LOG_CONFIG_FILE, True)
]
@pytest.mark.parametrize("test_input,expected", _BUILTIN_CONFIG_TEST_CASES)
def test_quick_logging_test_builtin_config_cases(caplog, test_input, expected):
    with caplog.at_level(logging.DEBUG):
        config_file = p3l.STDOUT_LOG_CONFIG_FILE
        assert p3l.quick_logging_test(THIS_APP_NAME,test_input) == expected, \
            f"Expected quick_logging_test({test_input}) to return {expected}"
    assert "warning message" in caplog.text, \
        "Expected 'warning message' in log output"
    assert "debug message" in caplog.text, \
        "Expected 'debug message' in log output"
    assert "info message" in caplog.text, \
        "Expected 'info message' in log output"
    assert "error message" in caplog.text, \
        "Expected 'error message' in log output"
    assert "critical message" in caplog.text, \
        "Expected 'critical message' in log output"
    assert "division by zero" in caplog.text, \
        "Expected 'division by zero' in log output"
    assert len(caplog.records) == 6
#endregion test_quick_logging_test_builtin_config_cases() function
# ---------------------------------------------------------------------------- +
#region test_quick_logging_test_with_STDOUT_ONLY() function
def test_quick_logging_test_with_STDOUT_ONLY(capsys):
    config_file: str = p3l.STDOUT_LOG_CONFIG_FILE
    # Apply the logging configuration from p3l.STDOUT_LOG_CONFIG_FILE
    assert p3l.quick_logging_test(THIS_APP_NAME, config_file), \
        f"Expected quick_logging_test({config_file}) to return True"
    captured = capsys.readouterr()
    assert "warning message" in captured.out, \
        "Expected 'warning message' in stdout output"
    assert "debug message" in captured.out, \
        "Expected 'debug message' in stdout output"
    assert "info message" in captured.out, \
        "Expected 'info message' in log output"
    assert "error message" in captured.out, \
        "Expected 'error message' in log output"
    assert "critical message" in captured.out, \
        "Expected 'critical message' in log output"
    assert "division by zero" in captured.out, \
        "Expected 'division by zero' in log output"    
#endregion test_quick_logging_test_with_STDOUT_ONLY() function
# ---------------------------------------------------------------------------- +
#region test_quick_logging_test_with_FORCE_EXCEPTION() function
def test_quick_logging_test_with_FORCE_EXCEPTION(capsys):
    config_file: str = p3l.FORCE_EXCEPTION
    # Apply the logging configuration from p3l.FORCE_EXCEPTION
    with pytest.raises(Exception) as excinfo:
        p3l.quick_logging_test(THIS_APP_NAME, config_file)
    assert p3l.FORCE_EXCEPTION_MSG in excinfo.value, \
        f"Expected Exception('{p3l.FORCE_EXCEPTION_MSG}')"
#endregion test_quick_logging_test_with_FORCE_EXCEPTION() function
# ---------------------------------------------------------------------------- +
#endregion Tests for quick_logging_test() function
# ---------------------------------------------------------------------------- +
