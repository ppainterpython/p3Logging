# ---------------------------------------------------------------------------- +
'''P3 Logging Module - simple add-on features to Python's logging module.
'''
# Python standard libraries
import atexit, pathlib, logging, inspect, logging.config  #, logging.handlers
# Python third-party libraries
import pyjson5
# Local libraries
from .p3LogConstants import *  
from .p3LogUtils import *
from .p3LogFormatters import JSONOutputFormatter, ModuleOrClassFormatter

# ---------------------------------------------------------------------------- +
#region retain_pytest_handlers decorator
def retain_pytest_handlers(f):
    '''A wrapper function to retain pytest handlers in the 
    logging configuration.'''
    # Attribution: Thanks to a-recknagel at 
    # https://github.com/pytest-dev/pytest/discussions/11618#discussioncomment-9699934
    # for this useful function.
    def wrapper(*args, **kwargs):
        pytest_handlers = [
            handler
            for handler in logging.root.handlers
            if handler.__module__ == "_pytest.logging"
        ]
        ret = f(*args, **kwargs)
        for handler in pytest_handlers:
            if handler not in logging.root.handlers:
                logging.root.addHandler(handler)
        return ret
    return wrapper
@retain_pytest_handlers
def wrap_config_dictConfig(log_config):
    try:
        # Now invoke the dictConfig function to apply the logging configuration
        logging.config.dictConfig(log_config)
    except Exception as e:
        # Exceptions from dictConfig can be deeply nested. The issues is 
        # most likely with the configuration json itself, not the logging module.
        m = f"Error: logging.config.dictConfig() "
        m += append_cause("",e)
        raise RuntimeError(m) from e
#endregion retain_pytest_handlers decorator
# ---------------------------------------------------------------------------- +
#region validate_file_logging() function
def validate_file_logging_config(config_json:dict) -> bool:
    '''Validate the file logging configuration.'''
    # Validate the JSON configuration
    try:
        _ = pyjson5.encode(config_json) # validate json serializable, not output
    except TypeError as e:
        t = type(config_json).__name__
        m = f"Error decoding config_json: '{config_json} as type: '{t}'"
        raise RuntimeError(m) from e
    except (pyjson5.JSONDecodeError, Exception) as e:
        m = f"Error decoding config_json input"
        raise RuntimeError(m) from e
    # Iterate handlers and check for file handlers
    file_handler_classes = ("logging.FileHandler", 
                            "logging.TimedRotatingFileHandler",
                            "logging.handlers.RotatingFileHandler")
    for name, handler in config_json["handlers"].items():
        if isinstance(handler, dict) and \
            handler.get("class") in file_handler_classes:
            # Check if the filename is valid
            filename = handler.get("filename")
            if filename:
                file_path = pathlib.Path(filename)
                # Ensure the directory exists
                file_path.parent.mkdir(parents=True, exist_ok=True)
                # Check if the file is writable
                try:
                    with open(file_path, "a"):
                        pass
                except IOError as e:
                    raise RuntimeError(f"Cannot write to log file: {file_path}") from e
#endregion validate_file_logging() function
# ---------------------------------------------------------------------------- +
#region validate_json_file() function
def validate_json_file(json_file:str) -> dict:
    '''Validate the file contains valid json, return it as str.'''
    # Check if the config file exists, is accessible, and is valid JSON
    json_file = pathlib.Path(json_file)
    if not json_file.exists():
        raise FileNotFoundError(f"JSON file '{json_file}' not found.")
    try:
        with open(json_file, "r") as f_in:
            config_json = pyjson5.decode_io(f_in)
            return config_json
    except TypeError as e:
        t = type(json_file).__name__
        m = f"Error accessing json_file: '{json_file} as type: '{t}'"
        raise RuntimeError(m) from e
    except FileNotFoundError as e:
        m = f"Error accessing json_file: '{json_file}'"
        raise RuntimeError(m) from e
    except pyjson5.JSONDecodeError as e:
        m = f"Error decoding json_file: '{json_file}'"
        raise RuntimeError(m) from e
    except Exception as e:
        m = f"Error processing json_file: '{json_file}'"
        raise RuntimeError(m) from e
    
#endregion validate_file_logging() function
# ---------------------------------------------------------------------------- +
#region setup_logging function
def setup_logging(config_file: str = STDOUT_LOG_CONFIG) -> None:
    """Set up logging for both stdout and a log file (thread-safe singleton)."""
    try:
        global log_config_dict
        # Validate and parse the json config_file
        at_log_config_json = validate_json_file(config_file)
        # For FileHandler types, validate the filenames included in the config
        validate_file_logging_config(at_log_config_json)
        # Apply the logging configuration preserving any pytest handlers
        wrap_config_dictConfig(at_log_config_json)
        log_config_dict = at_log_config_json

        # If the queue_handler is used, start the listener thread
        queue_handler = logging.getHandlerByName("queue_handler")
        if queue_handler is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)
    except Exception as e:
        print(f"{__name__}.setup_logging(): Error: Logging Setup {str(e)}")
        raise
#endregion setup_logging function
# ---------------------------------------------------------------------------- +
