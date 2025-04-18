#------------------------------------------------------------------------------+
'''
Constants for the P3 Logging (p3l) module.
'''
DEFAULT_LOG_FILE = "p3logging.log"
STDOUT_LOG_CONFIG_FILE = "stdout-only.jsonc"
STDOUT_FILE_LOG_CONFIG_FILE = "stdout-file.jsonc"
STDERR_FILE_JSON_LOG_CONFIG_FILE = "stderr-file-json.jsonc"
QUEUED_STDERR_FILE_JSON_LOG_CONFIG_FILE = "queued-stderr-file-json.jsonc"
FORCE_EXCEPTION = "force_exception"
FORCE_EXCEPTION_MSG = "Forced exception for testing purposes."

BUILTIN_LOGGING_CONFIG_FILES = [
    STDOUT_LOG_CONFIG_FILE,
    STDOUT_FILE_LOG_CONFIG_FILE,
    STDERR_FILE_JSON_LOG_CONFIG_FILE,
    QUEUED_STDERR_FILE_JSON_LOG_CONFIG_FILE
]

LOG_FLAG_PRINT_CONFIG_ERRORS = "print_config_errors"
LOG_FLAG_SETUP_COMPLETE = "setup_complete"