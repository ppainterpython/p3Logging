# ---------------------------------------------------------------------------- +
# test_p3LogInfo.py
# ---------------------------------------------------------------------------- +
#region imports
# python standard libraries
import logging, pytest

# third-party libraries
import inspect, pyjson5

# local libraries
import p3logging as p3l
#endregion imports
# ---------------------------------------------------------------------------- +
#region Globals
THIS_APP_NAME = "Test_p3LogInfo"

_BUILTIN_CONFIG_FILES_BOOL = [
    (p3l.STDOUT_LOG_CONFIG_FILE, True),
    (p3l.STDOUT_FILE_LOG_CONFIG_FILE, True),
    (p3l.STDERR_FILE_JSON_LOG_CONFIG_FILE, True),
    (p3l.QUEUED_STDERR_FILE_JSON_LOG_CONFIG_FILE, True)
]
_BUILTIN_CONFIG_FILES_DICT = [
    (p3l.STDOUT_LOG_CONFIG_FILE, dict),
    (p3l.STDOUT_FILE_LOG_CONFIG_FILE, dict),
    (p3l.STDERR_FILE_JSON_LOG_CONFIG_FILE, dict),
    (p3l.QUEUED_STDERR_FILE_JSON_LOG_CONFIG_FILE, dict)
]

root_logger = logging.getLogger()
logger = logging.getLogger(THIS_APP_NAME)
logger.propagate = True
#endregion Globals
# ---------------------------------------------------------------------------- +
#region TestShowLoggingSetup() Test Class
class TestShowLoggingSetup:
    """ Test class for show_logging_setup() function. """

    @pytest.mark.parametrize("test_input,expected", _BUILTIN_CONFIG_FILES_DICT)
    def test_show_logging_setup(self, capsys, test_input, expected):
        config_file = test_input
        # Invoke show_logging_setup() to display the current logging setup
        p3l.show_logging_setup(config_file)
        captured = capsys.readouterr()
        assert captured.out is not None, \
            "Expected show_logging_setup() to return a non-None value"
        assert isinstance(captured.out, str) and len(captured.out) > 0, \
            "Expected show_logging_setup() to return a non-zero str"
#endregion TestShowLoggingSetup() Test Class
# ---------------------------------------------------------------------------- +
#region Tests for p3LogConfig.get_Logger_config_info() function
# ---------------------------------------------------------------------------- +
#region test_get_logger_info() function
def test_get_Logger_config_info_STDOUT_LOG_CONFIG_FILE():
    config_file: str = p3l.STDOUT_LOG_CONFIG_FILE
    # Initialize the logger from a logging configuration file.
    # Apply the logging configuration from config_file
    p3l.setup_logging(THIS_APP_NAME, config_file, start_queue=False)
    # Invoke get_logger_info() to display the current logging setup
    res = p3l.get_Logger_config_info(indent = 0)
    # captured = capsys.readouterr()
    assert res is not None, \
        "Expected get_Logger_config_info() to return a non-None value"
    assert isinstance(res, str) and len(res) > 0, \
        "Expected get_Logger_config_info() to return a non-zero str"
    
#endregion test_get_logger_info() function
# ---------------------------------------------------------------------------- +
#region test_get_Logger_config_None_input() function
def test_get_Logger_config_None_input():
    config_file: str = p3l.STDOUT_LOG_CONFIG_FILE
    # Initialize the logger from a logging configuration file.
    # Apply the logging configuration from config_file
    log_configDict:dict = p3l.setup_logging(THIS_APP_NAME,
                                            config_file,
                                            start_queue=False,
                                            validate_only=True)
    # Invoke get_logger_info() with None input value
    res = p3l.get_Logger_config_info(log_configDict=None)
    # captured = capsys.readouterr()
    assert res is not None, \
        "Expected get_Logger_config_info(None) to return a non-None value"
    assert isinstance(res, str) and len(res) > 0, \
        "Expected get_Logger_config_info(None) to return a non-zero str"
#endregion test_get_Logger_config_None_input() function
# ---------------------------------------------------------------------------- +
#region test_get_Logger_config_empty_string_input() function
def test_get_Logger_config_empty_string_input():
    config_file: str = p3l.STDOUT_LOG_CONFIG_FILE
    # Initialize the logger from a logging configuration file.
    # Apply the logging configuration from config_file
    log_configDict:dict = p3l.setup_logging(THIS_APP_NAME,
                                            config_file,
                                            start_queue=False,
                                            validate_only=True)
    # Invoke get_logger_info() with None input value
    # Invoke get_logger_info() with "" input value
    with pytest.raises(TypeError) as excinfo:
        p3l.get_Logger_config_info(log_configDict="")
    expected_msg = "Invalid log_configDict: type:'str' value = ''"
    assert expected_msg in str(excinfo.value), \
        "Wrong message from expected TypeError for root_log_configDict=\"\""
    # captured = capsys.readouterr()
    
#endregion test_get_Logger_config_empty_string_input() function
# ---------------------------------------------------------------------------- +
#endregion Tests for p3LogConfig.get_Logger_config_info() function
# ---------------------------------------------------------------------------- +
#region Tests for p3LogConfig.get_Logger_root_config_info() function
# ---------------------------------------------------------------------------- +
#region test_get_Logger_root_config_info() function
def test_get_Logger_root_config_info():
    config_file: str = p3l.STDOUT_LOG_CONFIG_FILE
    cfm = f"Config file: '{config_file}'"
    # Initialize the logger from a logging configuration file.
    # Apply the logging configuration from config_file
    p3l.setup_logging(THIS_APP_NAME, config_file,start_queue=False)
    # Invoke get_logger_info() to display the current logging setup
    log_config = p3l.get_configDict()
    assert log_config is not None, \
        "Expected get_configDict() to return a non-None value"
    assert isinstance(log_config, dict) and len(log_config) > 0, \
        "Expected get_configDict() to return a non-zero dict"
    assert "root" in log_config, \
        "Expected get_configDict() to contain 'root' key"
    res = p3l.get_Logger_root_config_info(log_config['root'])
    assert res is not None, \
        "Expected get_root_Logger_config_info() to return a non-None value"
    assert isinstance(res, str) and len(res) > 0, \
        "Expected get_root_Logger_config_info() to return a non-zero str"
    assert "root config[" in res, \
        "Expected get_root_Logger_config_info() to contain 'root config['"
    # captured = capsys.readouterr() root config[
    
#endregion test_get_Logger_root_config_info() function
# ---------------------------------------------------------------------------- +
#region test_get_Logger_root_config_info_None() function
def test_get_Logger_root_config_info_None():
    res = p3l.get_Logger_root_config_info(root_log_configDict=None)
    assert (isinstance(res, str) and len(res) == 0), \
        "Expected empty string result for 'None' input to root_log_configDict"
#endregion test_get_Logger_root_config_info_None() function
# ---------------------------------------------------------------------------- +
#region test_get_Logger_root_config_info_wrong_type() function
def test_get_Logger_root_config_info_wrong_type():
    with pytest.raises(TypeError) as excinfo:
        p3l.get_Logger_root_config_info(root_log_configDict=101)
    expected_msg = "Invalid root_log_configDict: type:'int' value = '101'"
    assert expected_msg in str(excinfo.value), \
        "Wrong message from expected TypeError for root_log_configDict=101"
#endregion test_get_Logger_root_config_info_wrong_type() function
# ---------------------------------------------------------------------------- +
#region test_get_logger_info() function
def test_get_logger_info_showall_STDOUT_LOG_CONFIG_FILE():
    config_file: str = p3l.STDOUT_LOG_CONFIG_FILE
    cfm = f"Config file: '{config_file}'"
    # Initialize the logger from a logging configuration file.
    # Apply the logging configuration from config_file
    p3l.setup_logging(THIS_APP_NAME, config_file,start_queue=False)
    # Invoke get_logger_info() to display the current logging setup
    res = p3l.get_logger_info(logging.getLogger(), 0, showall=True)
    assert res is not None, \
        "Expected get_logger_info() to return a non-None value"
    assert isinstance(res, str) and len(res) > 0, \
        "Expected get_logger_info() to return a non-zero str"
    
#endregion test_get_logger_info() function
# ---------------------------------------------------------------------------- +
#region test_get_logger_info_one_line() function
def test_get_logger_info_one_line_STDOUT_LOG_CONFIG_FILE():
    config_file: str = p3l.STDOUT_LOG_CONFIG_FILE
    cfm = f"Config file: '{config_file}'"
    # Initialize the logger from a logging configuration file.
    # Apply the logging configuration from config_file
    p3l.setup_logging(THIS_APP_NAME, config_file,start_queue=False)
    # Invoke get_logger_info() to display the current logging setup
    res = p3l.get_logger_info(logging.getLogger(), 0, showall=False)
    assert res is not None, \
        "Expected get_logger_info() to return a non-None value"
    assert isinstance(res, str) and len(res) > 0, \
        "Expected get_logger_info() to return a non-zero str"
    
#endregion test_get_logger_info_one_line() function
# ---------------------------------------------------------------------------- +
#endregion Tests for p3LogConfig.get_Logger_root_config_info() function
# ---------------------------------------------------------------------------- +
#region Tests for quick_logging_test() function
# ---------------------------------------------------------------------------- +
#region test_quick_logging_test_STDERR_FILE_JSON_LOG_CONFIG_FILE() function
def test_quick_logging_test_STDERR_FILE_JSON_LOG_CONFIG_FILE(caplog):
    ln : str = THIS_APP_NAME
    with caplog.at_level(logging.DEBUG):
        config_file = p3l.STDERR_FILE_JSON_LOG_CONFIG_FILE
        p3l.quick_logging_test(ln, config_file, reload =  True)
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
#endregion test_quick_logging_test_STDERR_FILE_JSON_LOG_CONFIG_FILE() function
# ---------------------------------------------------------------------------- +
#region test_quick_logging_test_cases() function
@pytest.mark.parametrize("test_input,expected", _BUILTIN_CONFIG_FILES_BOOL)
def test_quick_logging_test_cases(caplog, test_input, expected):
    ln : str = THIS_APP_NAME
    with caplog.at_level(logging.DEBUG):
        config_file = p3l.STDOUT_LOG_CONFIG_FILE
    assert p3l.quick_logging_test(ln, test_input, reload = True) == expected, \
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
#endregion test_quick_logging_test_cases() function
# ---------------------------------------------------------------------------- +
#endregion Tests for quick_logging_test() function
# ---------------------------------------------------------------------------- +
#region Local __main__ stand-alone
if __name__ == "__main__":
    try:
        test_get_logger_info_one_line_STDOUT_LOG_CONFIG_FILE()
        test_get_logger_info_showall_STDOUT_LOG_CONFIG_FILE()
    except Exception as e:
        print(str(e))
        exit(1)
#endregion
# ---------------------------------------------------------------------------- +
