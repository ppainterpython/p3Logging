# ---------------------------------------------------------------------------- +
# test_p3LogConfig.py
# ---------------------------------------------------------------------------- +
#region imports
# python standard libraries
import logging, pytest
from pathlib import Path

# third-party libraries
import inspect, pyjson5
from concurrent_log_handler import ConcurrentRotatingFileHandler

# local libraries
import p3_utils as p3u
import p3logging as p3l
#endregion imports
# ---------------------------------------------------------------------------- +
#region Globals
THIS_APP_NAME = "Test_p3Config"

# For tests of builtin config files for functions returning a dictionary
_BUILTIN_CONFIG_FILES_DICT = [
    (p3l.STDOUT_LOG_CONFIG_FILE, dict),
    (p3l.STDOUT_FILE_LOG_CONFIG_FILE, dict),
    (p3l.STDERR_FILE_JSON_LOG_CONFIG_FILE, dict),
    (p3l.QUEUED_STDERR_FILE_JSON_LOG_CONFIG_FILE, dict)
]
# For tests of builtin config files for functions returning a bool
_BUILTIN_CONFIG_FILES_BOOL = [
    (p3l.STDOUT_LOG_CONFIG_FILE, True),
    (p3l.STDOUT_FILE_LOG_CONFIG_FILE, True),
    (p3l.STDERR_FILE_JSON_LOG_CONFIG_FILE, True),
    (p3l.QUEUED_STDERR_FILE_JSON_LOG_CONFIG_FILE, True)
]

root_logger = logging.getLogger()
logger = logging.getLogger(THIS_APP_NAME)
logger.propagate = True
#endregion Globals
# ---------------------------------------------------------------------------- +
#region TestValidateDictConfig) Test Class
class TestValidateDictConfig:
    """ Test the validate_dictConfig() function in various ways. """
    # ------------------------------------------------------------------------ +
    #region test_validate_dictConfig_for_builtin_config_files() method
    @pytest.mark.parametrize("test_input,expected", 
                            _BUILTIN_CONFIG_FILES_BOOL)
    def test_validate_dictConfig_for_builtin_config_files(self,
                                                test_input, expected) -> None:
        # Test with the builtin config files, happy path
        config_file = test_input
        assert isinstance((dictConfig := p3l.validate_config_file(config_file)), dict), \
            f"Expected validate_config_file({config_file}) to return type: 'dict'"
        assert p3l.validate_dictConfig(dictConfig) == expected, \
            f"Expected validate_dictConfig({config_file}) to return type: '{expected}'"
    #endregion test_validate_dictConfig_for_builtin_config_files() method
    # ------------------------------------------------------------------------ +
    #region test_validate_dictConfig_FORCED_EXCEPTION() method
    def test_validate_dictConfig_FORCED_EXCEPTION(self):
        dictConfig: str = p3u.FORCE_EXCEPTION
        # Apply the logging configuration from p3u.FORCE_EXCEPTION
        with pytest.raises(Exception) as excinfo:
            p3l.validate_dictConfig(dictConfig)
        em = "testcase: Default Exception Test for func:validate_dictConfig()"
        assert em in str(excinfo.value), \
            f"Expected '{em}' in exception message, " \
            f"but got '{str(excinfo.value)}'"
    #endregion test_validate_dictConfig_FORCED_EXCEPTION() method
    # ------------------------------------------------------------------------ +
#endregion TestValidateDictConfig) Test Class
# ---------------------------------------------------------------------------- +
#region TestValidateConfigFile() Test Class
class TestValidateConfigFile:
    """ Test the validate_config_file() function in various ways. """
    # ------------------------------------------------------------------------ +
    #region test_validate_dictConfig_for_builtin_config_files() function
    @pytest.mark.parametrize("test_input,expected", 
                            _BUILTIN_CONFIG_FILES_DICT)
    def test_validate_config_file_for_builtin_config_files(self,
                                                test_input, expected) -> None:
        # Test with the builtin config files, happy path
        config_file = test_input
        assert isinstance((p3l.validate_config_file(config_file)), expected), \
            f"Expected validate_config_file({config_file}) to return type: '{expected}'"
    #endregion test_validate_dictConfig_for_builtin_config_files() function
    # ------------------------------------------------------------------------ +
    #region test_validate_config_file_exceptions() method
    def test_validate_config_file_exceptions(self):
        """ Test the validate_dictConfig() function with invalid input. """
        # Test with invalid config_file name
        config_file = "test_configs/foo_invalid_config_file.jsonc"
        with pytest.raises(FileNotFoundError) as excinfo:
            p3l.validate_config_file(config_file)
        assert f"Config file not found:'{config_file}'" in str(excinfo.value), \
            f"Expected validate_config_file({config_file}) to raise FileNotFoundError"
        # Test with invalid config_file input type None
        config_file = None
        with pytest.raises(TypeError) as excinfo:
            p3l.validate_config_file(config_file)
        em = f"Invalid path_name: type:'<class 'NoneType'>' value = 'None'"
        assert em in str(excinfo.value), \
            f"Expected exception message to include: '{em}'"
        # Test with config file containing invalid JSON text
        config_file = "tests/test_configs/invalid-json.jsonc"
        with pytest.raises(pyjson5.Json5IllegalCharacter) as excinfo:
            p3l.validate_config_file(config_file)
    #endregion test_validate_config_file_exceptions() method
    # ------------------------------------------------------------------------ +
    #region test_validate_config_file_FORCED_EXCEPTION() method
    def test_validate_config_file_FORCED_EXCEPTION(self):
        config_file: str = p3u.FORCE_EXCEPTION
        # Apply the logging configuration from p3u.FORCE_EXCEPTION
        with pytest.raises(Exception) as excinfo:
            p3l.validate_config_file(config_file)
        em = "testcase: Default Exception Test for func:validate_config_file()"
        assert em in str(excinfo.value), \
            f"Expected '{em}' in exception message, " \
            f"but got '{str(excinfo.value)}'"
    #endregion test_validate_config_file_FORCED_EXCEPTION() method
    # ------------------------------------------------------------------------ +
    # ------------------------------------------------------------------------ +
    # ------------------------------------------------------------------------ +
# ---------------------------------------------------------------------------- +
# ---------------------------------------------------------------------------- +
#endregion TestValidateConfigFile() Test Class
# ---------------------------------------------------------------------------- +
#region TestSetupLogging() Test Class
# ---------------------------------------------------------------------------- +
class TestSetupLogging:
    """ Test the setup_logging() function in various ways. """
    # ------------------------------------------------------------------------ +
    #region test_setup_logging_simple() method
    def test_setup_logging_simple(self):
        # Test the setup_logging() function with a valid config file
        config_file = p3l.STDOUT_LOG_CONFIG_FILE
        assert isinstance((log_config_dict := p3l.setup_logging(config_file)), dict), \
            f"Expected setup_logging({config_file}) to return type: 'dict'"
        assert p3l.get_config_path() is not None, \
            f"Expected get_config_path() to return a Path object, not None."
        assert isinstance(p3l.get_config_path(), Path), \
            f"Expected Path object, but got {type(p3l.get_config_path())}"
    #endregion test_setup_logging_simple() method
    # ------------------------------------------------------------------------ +
    #region test_setup_logging_for_builting_config_files() method
    @pytest.mark.parametrize("test_input,expected", 
                            _BUILTIN_CONFIG_FILES_DICT)
    def test_setup_logging_for_builtin_config_files(self, caplog, 
                                                     test_input, expected) -> None:
        """ Test the setup_logging() with each of the builtin logging config files. 
        
        Constants are defined to reference the builtin logging config files.
        Test each one for a happy path completion to setup logging for each.
        Clear the logging config after each test and include some logging calls
        to validate.

        Args:
            test_input (str): The name of the logging config file.
            expected (dict|None): The expected type of the return value.
        """
        # Test the builtin logging config files
        ln = THIS_APP_NAME
        assert isinstance((log_config_dict := p3l.setup_logging(ln,test_input)), expected), \
            f"Expected setup_logging({test_input}) to return type: '{expected}'"
        assert (config_file_path := p3l.get_config_path()) is not None, \
            f"Expected get_config_path() to return a Path object."
        assert isinstance(config_file_path, Path), \
            f"Expected Path object, but got {type(config_file_path)}"
    #endregion test_setup_logging_for_builting_config_files() method
    # ------------------------------------------------------------------------ +
    #region test_setup_logging_invalid_config_file_parameter() method
    def test_setup_logging_invalid_config_file_parameter(self) -> None:
        """ Test the setup_logging() with invalid config_file parameters. """
        # Test with invalid config_file name
        config_file = "invalid_config_file.jsonc"
        with pytest.raises(FileNotFoundError) as excinfo:
            p3l.setup_logging(THIS_APP_NAME,config_file)
        assert f"Config file not found:'{config_file}'" in str(excinfo.value), \
            f"Expected setup_logging({config_file}) to return type: 'dict'"
    #endregion test_setup_logging_invalid_config_file_parameter() method
    # ------------------------------------------------------------------------ +
    #region test_setup_logging_None_config_file_parameter() method
    def test_setup_logging_None_config_file_parameter(self) -> None:
        """ Test the setup_logging() with None config_file parameters. """
        # Test with invalid config_file input type None
        config_file = None
        with pytest.raises(TypeError) as excinfo:
            p3l.setup_logging(THIS_APP_NAME,config_file)
        em = f"Invalid path_name: type:"
        assert em in str(excinfo.value), \
            f"Expected exception message to include: '{em}'"
    #endregion test_setup_logging_None_config_file_parameter() method
    # ------------------------------------------------------------------------ +
    #region test_setup_validate_only() method
    @pytest.mark.parametrize("test_input,expected", 
                            _BUILTIN_CONFIG_FILES_DICT)
    def test_setup_validate_only(self, test_input, expected) -> None:
        """ Test the setup_logging() validate_only parameters. """
        # Test with invalid config_file input type None
        ln = THIS_APP_NAME
        assert isinstance((log_config_dict := 
                        p3l.setup_logging(ln, test_input,validate_only=True)), expected), \
            f"Expected setup_logging({test_input}) to return type: '{expected}'"
    #endregion test_setup_validate_only() method
    # ------------------------------------------------------------------------ +
    #region test_setup_logging_with_FileHandler_filenames_input() method
    def test_setup_logging_with_FileHandler_filenames_input(self):
        # Initialize the logger from a logging configuration file.
        filenames = {"file": "logs/p3logging-file-test.log", 
                    "json_file": "logs/p3logging-json_file-test.log"}
        config_file: str = p3l.STDOUT_FILE_LOG_CONFIG_FILE
        r : bool = True # reload flag
        ln : str = THIS_APP_NAME # Logger Name
        assert p3l.quick_logging_test(ln, config_file, filenames, r), \
            f"Expected quick_logging_test({config_file}) to return True"
        config_file: str = p3l.STDERR_FILE_JSON_LOG_CONFIG_FILE
        assert p3l.quick_logging_test(ln, config_file,filenames, r), \
            f"Expected quick_logging_test({config_file}) to return True"
    #endregion test_setup_logging_with_FileHandler_filenames_input() method
    # ------------------------------------------------------------------------ +
#endregion TestSetupLogging() Test Class
# ---------------------------------------------------------------------------- +
#region TestQuickLoggingTest Test Class
class TestQuickLoggingTest:
    """ Test the quick_logging_test() function in various ways. """
    # ------------------------------------------------------------------------ +
    #region test_quick_logging_test_builtin_config_cases() function
    @pytest.mark.parametrize("test_input,expected", _BUILTIN_CONFIG_FILES_BOOL)
    def test_quick_logging_test_builtin_config_cases(self, caplog, test_input, expected) -> None:
        with caplog.at_level(logging.DEBUG):
            config_file = p3l.STDOUT_LOG_CONFIG_FILE
        ln : str = THIS_APP_NAME # Logger Name
        assert p3l.quick_logging_test(ln,test_input,reload=True) == expected, \
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
    # ------------------------------------------------------------------------ +
    #region test_quick_logging_test_with_STDOUT_ONLY() method
    def test_quick_logging_test_with_STDOUT_ONLY(self, capsys):
        config_file: str = p3l.STDOUT_LOG_CONFIG_FILE
        # Apply the logging configuration from p3l.STDOUT_LOG_CONFIG_FILE
        ln : str = THIS_APP_NAME # Logger Name
        assert p3l.quick_logging_test(ln, config_file, reload = True), \
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
        # Test with invalid app_name
        with pytest.raises(TypeError) as excinfo:
            p3l.quick_logging_test(None, config_file)
        em = "Invalid app_name: type(NoneType) value = 'None'"
        assert em in str(excinfo.value), \
            f"Expected 'Invalid app_name: type:'<class 'NoneType'>' value = 'None'" 
    #endregion test_quick_logging_test_with_STDOUT_ONLY() method
    # ------------------------------------------------------------------------ +
    #region test_quick_logging_test_with_FORCE_EXCEPTION() method
    def test_quick_logging_test_with_FORCE_EXCEPTION(self):
        config_file: str = p3u.FORCE_EXCEPTION
        # Apply the logging configuration from p3u.FORCE_EXCEPTION
        with pytest.raises(Exception) as excinfo:
            p3l.quick_logging_test(p3u.FORCE_EXCEPTION, config_file)
        em = "testcase: RuntimeError Exception Test for func:quick_logging_test()"
        assert em in str(excinfo.value), \
            f"Expected '{em}' in exception message, " \
            f"but got '{str(excinfo.value)}'"
    #endregion test_quick_logging_test_with_FORCE_EXCEPTION() method
    # ------------------------------------------------------------------------ +
# ---------------------------------------------------------------------------- +
#endregion TestQuickLoggingTest Test Class
# ---------------------------------------------------------------------------- +
#region TestLogFlags() Test Class
class TestLogFlags:
    """ Test the log flags functions in various ways. """
    # ------------------------------------------------------------------------ +
    #region test_get_log_flags() method
    def test_log_flags(self):
        # Test the log flags functions: get, set, etc.
        ln = THIS_APP_NAME
        assert p3l.setup_logging(ln, p3l.STDOUT_LOG_CONFIG_FILE) is not None, \
            str(f"Expected setup_logging({ln,p3l.STDOUT_LOG_CONFIG_FILE}) " 
            f"to return the log_config_dict")
        assert (log_flags := p3l.get_log_flags()) is not None, \
            f"Expected get_log_flags() to return a log flag dictionary."
        assert isinstance(log_flags, dict), \
            f"Expected get_log_flags() to return a dictionary."
        assert p3l.LOG_FLAG_PRINT_CONFIG_ERRORS in log_flags, \
            str(f"Expected get_log_flags() to have key: "
                f"'{p3l.LOG_FLAG_PRINT_CONFIG_ERRORS}' corresponding to "
                f"constant 'p3l.LOG_FLAG_PRINT_CONFIG_ERRORS'")
        assert p3l.LOG_FLAG_SETUP_COMPLETE in log_flags, \
            str(f"Expected get_log_flags() to have key: "
                f"'{p3l.LOG_FLAG_SETUP_COMPLETE}' corresponding to "
                f"constant 'p3l.LOG_FLAG_SETUP_COMPLETE'")
        assert isinstance((lfpce := log_flags[p3l.LOG_FLAG_PRINT_CONFIG_ERRORS]), bool), \
            f"Expected get_log_flags() to return a boolean value for key: " \
            f"'{p3l.LOG_FLAG_PRINT_CONFIG_ERRORS}'"
        assert isinstance((lfsc := log_flags[p3l.LOG_FLAG_SETUP_COMPLETE]), bool), \
            f"Expected get_log_flags() to return a boolean value for key: " \
            f"'{p3l.LOG_FLAG_SETUP_COMPLETE}'"
        assert p3l.set_log_flag(p3l.LOG_FLAG_PRINT_CONFIG_ERRORS, not lfpce) is None, \
            f"Expected set_log_flag({p3l.LOG_FLAG_PRINT_CONFIG_ERRORS}, not lfpce) " \
            f"to return None"
        assert p3l.set_log_flag(p3l.LOG_FLAG_SETUP_COMPLETE, not lfsc) is None, \
            f"Expected set_log_flag({p3l.LOG_FLAG_SETUP_COMPLETE}, not lfsc) " \
            f"to return None"
        assert bool(p3l.get_log_flag(p3l.LOG_FLAG_PRINT_CONFIG_ERRORS)) == (not bool(lfpce)), \
            f"Expected get_log_flag({p3l.LOG_FLAG_PRINT_CONFIG_ERRORS}) to return " \
            f"{not bool(lfpce)}"
        assert bool(p3l.get_log_flag(p3l.LOG_FLAG_PRINT_CONFIG_ERRORS)) == (not bool(lfpce)), \
            f"Expected get_log_flag({p3l.LOG_FLAG_PRINT_CONFIG_ERRORS}) to return " \
            f"{not bool(lfpce)}"
    #endregion test_get_log_flags() method
    # ------------------------------------------------------------------------ +
    #region test_log_flags_exceptions() method
    def test_log_flags_exceptions(self):    
        assert p3l.set_log_flag(p3l.LOG_FLAG_PRINT_CONFIG_ERRORS, True) is None, \
            f"Expected set_log_flag({p3l.LOG_FLAG_PRINT_CONFIG_ERRORS}, True) " \
            f"to return None"
        with pytest.raises(KeyError) as excinfo:
            p3l.get_log_flag("invalid_flag")
        assert "invalid_flag" in str(excinfo.value)
        with pytest.raises(KeyError) as excinfo:
            p3l.set_log_flag("invalid_flag", True)
        assert "invalid_flag" in str(excinfo.value), \
            f"Expected 'Invalid log flag key:' in KeyError message"
        with pytest.raises(TypeError) as excinfo:
            p3l.set_log_flag(p3l.LOG_FLAG_PRINT_CONFIG_ERRORS, "invalid_value")
        assert "invalid_value" in str(excinfo.value), \
            f"Expected 'invalid_value' in TypeError message"  
        # Force an exception to be raised
        with pytest.raises(Exception) as excinfo:
            p3l.set_log_flag((1,2,3), "invalid_value")
        assert "Invalid log flag key:" in str(excinfo.value), \
            f"Expected 'Invalid log flag key:' in TypeError message"  
    #endregion test_log_flags_exceptions() method
    # ------------------------------------------------------------------------ +
#endregion TestLogFlags() Test Class
# ---------------------------------------------------------------------------- +
#region TestHelperFunctions() Test Class
class TestHelperFunctions:
    """ Test the helper functions in various ways. """
    # ------------------------------------------------------------------------ +
    #region test_is_config_file_reachable() method
    @pytest.mark.parametrize("test_input,expected", _BUILTIN_CONFIG_FILES_BOOL)
    def test_is_config_file_reachable(self, test_input, expected):
        """ Test the p3logging builtin log config files are reachable. """

        # Test the filename only input case
        assert isinstance((test_path := p3l.is_config_file_reachable(test_input)), 
                        (Path, type(None))), \
            f"Expected is_config_file_reachable({str(test_input)}) to return Path|None, " \
            f"but got {type(test_path)}"
        assert test_path.name == test_input, \
            f"Expected is_config_file_reachable({str(test_input)}) to return {test_input}, " \
            f"but got {test_path.name}"
        # Test absolute path case
        assert isinstance((abs_path := test_path.absolute()), Path), \
            f"Expected is_config_file_reachable({str(test_input)}) to return Path, " \
            f"but got {type(abs_path)}"
        assert abs_path.exists(), \
            f"Expected Path: '{abs_path.absolute()}' to exist."
        assert isinstance((test_path2 := p3l.is_config_file_reachable(str(abs_path))), 
                        (Path, type(None))), \
            f"Expected is_config_file_reachable({str(test_path2)}) to return Path|None, " \
            f"but got {type(test_path2)}"
        assert test_path2.name == test_path.name, \
            f"Expected is_config_file_reachable({str(test_path2)}) to return {test_path.name}, " \
            f"but got {test_path2.name}"
        # Test the relative path case
        # cwd = Path.cwd()
        # rel_path = cwd / "src/p3logging/p3logging_configs" / test_input
        rel_path = "src/p3logging/p3logging_configs/" + test_input
        assert isinstance((test_path2 := p3l.is_config_file_reachable(str(rel_path))), 
                        (Path, type(None))), \
            f"Expected is_config_file_reachable({str(test_path2)}) to return Path|None, " \
            f"but got {type(test_path2)}"
        assert test_path2.name == test_path.name, \
            f"Expected is_config_file_reachable({str(test_path2)}) to return {test_path.name}, " \
            f"but got {test_path2.name}"
    #endregion test_is_config_file_reachable() method
    # ------------------------------------------------------------------------ +
    #region test_is_config_file_reachable_exceptions() method
    def test_is_config_file_reachable_exceptions(self):
        """ Test the exception handling. """
        # Test non-existent path_name path case
        assert p3l.is_config_file_reachable("non_existent_path") is None, \
            "Expected is_config_file_reachable('non_existent_path') to return None"
        assert p3l.is_config_file_reachable("/path/to/nowhere") is None, \
            "Expected is_config_file_reachable('/path/to/nowhere') to return None"
        # Get test_path to work with later
        test_path_name = p3l.STDOUT_LOG_CONFIG_FILE
        assert isinstance((test_path := p3l.is_config_file_reachable(test_path_name)), 
                        (Path, type(None))), \
            f"Expected is_config_file_reachable({str(test_path_name)}) to return Path|None, " \
            f"but got {type(test_path)}"
        # Test path_name = None case
        with pytest.raises(TypeError) as excinfo:
            p3l.is_config_file_reachable(None)
        expected_msg = "Invalid path_name: type:'<class 'NoneType'>' value = 'None'"
        assert str(excinfo.value) == expected_msg, \
            f"Expected TypeError with message '{expected_msg}', " \
            f"but got '{str(excinfo.value)}'"
        # Test path_name = "" case
        with pytest.raises(TypeError) as excinfo:
            p3l.is_config_file_reachable("")
        expected_msg = "Invalid path_name: type:'<class 'str'>' value = ''"
        assert str(excinfo.value) == expected_msg, \
            f"Expected TypeError with message '{expected_msg}', " \
            f"but got '{str(excinfo.value)}'"
        # Test path_name = int case
        with pytest.raises(TypeError) as excinfo:
            p3l.is_config_file_reachable(123)
        expected_msg = "Invalid path_name: type:'<class 'int'>' value = '123'"
        assert str(excinfo.value) == expected_msg, \
            f"Expected TypeError with message '{expected_msg}', " \
                f"but got '{str(excinfo.value)}'"
    #endregion test_is_config_file_reachable_exceptions() method
    # ------------------------------------------------------------------------ +
    #region test_is_config_file_reachable_input_None() method
    def test_is_config_file_reachable_input_None(self):
        """ Test the input is None case. """
        # Test path_name = None case
        with pytest.raises(TypeError) as excinfo:
            p3l.is_config_file_reachable(None)

    #endregion test_is_config_file_reachable_input_None() method
    # ------------------------------------------------------------------------ +
    #region test_exc_msg() method
    def test_exc_msg(self):
        # Test with a valid exception
        try:
            raise ValueError("Test exception")
        except Exception as e:
            result = p3l.exc_msg(self.test_exc_msg,e)
            assert "Test exception" in result, \
                f"Expected 'Test exception' in {result}"

        # Test with invalid function 
        result = p3l.exc_msg(None, None)
        em = "Invalid func param:'None'"
        assert em in result, \
            f"Expected 'exc_msg(): Invalid func param:'None'' but got {result}"

        # Test with a forced exception
        e = ZeroDivisionError("testcase: test_exc_msg()")
        with pytest.raises(ZeroDivisionError) as excinfo:
            result = p3l.exc_msg(p3u.force_exception, "test_exc_msg():")
        exp_msg = f"testcase: Default Exception Test for func:force_exception()"
        assert exp_msg in str(excinfo.value), \
            f"Expected Exception msg to be '{exp_msg}' but got '{str(excinfo.value)}'"
    #endregion test_exc_msg() method
#endregion TestHelperFunctions() Test Class
# ---------------------------------------------------------------------------- +
