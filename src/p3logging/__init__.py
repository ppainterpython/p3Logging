""" p3logging Module - simple add-on features to Python's logging module. """
__version__ = "0.2.0"
__author__ = "Paul Painter"
from .p3logging_constants import (
    STDOUT_LOG_CONFIG_FILE,
    STDOUT_FILE_LOG_CONFIG_FILE,
    STDERR_FILE_JSON_LOG_CONFIG_FILE,
    QUEUED_STDERR_FILE_JSON_LOG_CONFIG_FILE,
    BUILTIN_LOGGING_CONFIG_FILES,
    DEFAULT_LOGGER_NAME,
    DEFAULT_LOG_FILE,
    FORCE_EXCEPTION,
    FORCE_EXCEPTION_MSG,
    LOG_FLAG_PRINT_CONFIG_ERRORS,
    LOG_FLAG_SETUP_COMPLETE
)

from .p3logging_config import (
    get_configDict, get_config_path,
    get_file_handler_property,
    setup_logging, update_FileHandler_filenames, start_queue, stop_queue,
    get_formatter_id_by_custom_class_name, quick_logging_test,
    get_Logger_config_info, get_Logger_root_config_info,
    get_logger_formatters, get_log_flag, set_log_flag,
    get_config_path, get_log_flags, is_config_file_reachable,
    validate_config_file, validate_dictConfig
    )

from .p3logging_formatters import JSONOutputFormatter, ModuleOrClassFormatter

from .p3logging_info import get_QueueHandler_info, get_logger_filter_info, \
    get_logger_handler_info, get_logger_info, \
    show_logging_setup

__all__ = [
    "STDOUT_LOG_CONFIG_FILE",
    "STDOUT_FILE_LOG_CONFIG_FILE",
    "STDERR_FILE_JSON_LOG_CONFIG_FILE",
    "QUEUED_STDERR_FILE_JSON_LOG_CONFIG_FILE",
    "BUILTIN_LOGGING_CONFIG_FILES",
    "DEFAULT_LOGGER_NAME",
    "DEFAULT_LOG_FILE",
    "FORCE_EXCEPTION",
    "FORCE_EXCEPTION_MSG",
    "LOG_FLAG_PRINT_CONFIG_ERRORS",
    "LOG_FLAG_SETUP_COMPLETE",
    "get_QueueHandler_info",
    "get_logger_filter_info", 
    "get_logger_handler_info",
    "get_logger_info",
    "show_logging_setup",
    "get_log_flags",
    "get_log_flag",
    "set_log_flag",
    "get_config_path",
    "validate_config_file",
    "validate_dictConfig",
    "get_configDict",
    "get_config_path",
    "get_file_handler_property",
    "setup_logging",
    "update_FileHandler_filenames",
    "start_queue",
    "stop_queue",
    "get_formatter_id_by_custom_class_name",
    "quick_logging_test",
    "get_Logger_config_info",
    "get_Logger_root_config_info",
    "get_logger_formatters",
    "JSONOutputFormatter",
    "ModuleOrClassFormatter",
]