""" P3 Logging Module - simple add-on features to Python's logging module. """
__version__ = "0.1.0"
__author__ = "Paul Painter"

from .p3LogConstants import \
    STDOUT_LOG_CONFIG_FILE, \
    STDOUT_FILE_LOG_CONFIG_FILE, \
    STDERR_FILE_JSON_LOG_CONFIG_FILE, \
    QUEUED_STDERR_FILE_JSON_LOG_CONFIG_FILE, \
    BUILTIN_LOGGING_CONFIG_FILES, \
    DEFAULT_LOG_FILE, \
    FORCE_EXCEPTION, \
    FORCE_EXCEPTION_MSG

from .p3LogUtils import is_filename_only, is_config_file_reachable, \
    append_cause, fpfx, exc_msg

from .p3LogConfig import get_configDict, get_config_path, \
    get_file_handler_property, \
    setup_logging, update_FileHandler_filenames, start_queue, stop_queue, \
    get_formatter_id_by_custom_class_name, quick_logging_test, \
    get_Logger_config_info, get_Logger_root_config_info, \
    get_logger_formatters

from .p3LogFormatters import JSONOutputFormatter, ModuleOrClassFormatter

from .p3LogInfo import get_QueueHandler_info, get_logger_filter_info, \
    get_logger_handler_info, get_logger_info, \
    show_logging_setup

__all__ = [
    "STDOUT_LOG_CONFIG_FILE",
    "STDOUT_FILE_LOG_CONFIG_FILE",
    "STDERR_FILE_JSON_LOG_CONFIG_FILE",
    "QUEUED_STDERR_FILE_JSON_LOG_CONFIG_FILE",
    "BUILTIN_LOGGING_CONFIG_FILES",
    "DEFAULT_LOG_FILE",
    "FORCE_EXCEPTION",
    "FORCE_EXCEPTION_MSG",
    "is_filename_only",
    "is_config_file_reachable",
    "append_cause",
    "fpfx",
    "exc_msg",
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