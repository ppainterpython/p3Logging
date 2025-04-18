# ---------------------------------------------------------------------------- +
""" P3 Logging Module - simple add-on features to Python's logging module. """
#region imports
# Python standard libraries
import atexit, pathlib, logging, inspect, logging.config 
from pathlib import Path
from typing import List
# Python third-party libraries
import pyjson5
# Local libraries
from .p3LogConstants import *
from .p3LogUtils import log_exc, fpfx, is_path_reachable, append_cause
#endregion imports
# ---------------------------------------------------------------------------- +
#region Globals
_log_config_dict = {}
_log_config_path = None
_log_flags = {
        LOG_FLAG_PRINT_CONFIG_ERRORS: True,
        LOG_FLAG_SETUP_COMPLETE: False
}
#endregion Globals
# ---------------------------------------------------------------------------- +
#region get_log_flags() function
def get_log_flags() -> dict:
    """Return the current log flags dictionary."""
    global _log_flags
    return _log_flags
#endregion get_log_flags() function
# ---------------------------------------------------------------------------- +
#region get_log_flag() function
def get_log_flag(flag_key:str) -> bool:
    """Return the valid log flag value.
    
    Args:
        flag_key (str): The key of the log flag to retrieve.

    Returns:
        bool: The value of the specified log flag.

    Raises:
        KeyError: If the flag_key is not found in the log flags dictionary.    
        TypeError: If the flag_key is not a string.
    """
    global _log_flags
    return _log_flags[flag_key]
#endregion get_log_flags() function
# ---------------------------------------------------------------------------- +
#region set_log_flag() function
def set_log_flag(flag_key:str,flag_value:bool=False) -> None:
    """Set the valid log flag value.
    
    Args:
        flag_key (str): The key of the log flag to set.
        flag_value (bool): The value to set the log flag to.

    Returns:
        None: 

    Raises:
        KeyError: If the flag_key is not found in the log flags dictionary.    
        TypeError: If the flag_key is not a string.
    """
    global _log_flags
    if flag_key not in _log_flags:
        raise KeyError(f"Invalid log flag key: '{flag_key}'")
    if not isinstance(flag_value, bool):
        raise TypeError(f"Invalid log flag value: '{flag_value}'")
    _log_flags[flag_key] = flag_value
    return None
#endregion set_log_flags() function
# ---------------------------------------------------------------------------- +
#region get_configDict() function
def get_configDict() -> dict:
    """Return the current dictConfig() logging configuration dictionary."""
    global _log_config_dict
    return _log_config_dict
#endregion get_configDict() function
# ---------------------------------------------------------------------------- +
#region get_config_path() function
def get_config_path() -> dict:
    """Return the current logging configuration file path."""
    global _log_config_path
    return _log_config_path
#endregion get_config_path() function
# ---------------------------------------------------------------------------- +
#region get_file_handler_property() function
def get_file_handler_property(handler_name:str, property_name:str) -> str:
    """Get the value of a property from a file handler."""
    #TODO: get_file_handler_property() implementation
    raise NotImplementedError("get_file_handler_property() not implemented")
#endregion get_file_handler_property()
# ---------------------------------------------------------------------------- +
#region retain_pytest_handlers
def retain_pytest_handlers(f):
    """
    A wrapper function to retain pytest handlers in the 
    logging configuration.
    """
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
#endregion retain_pytest_handlers
# ---------------------------------------------------------------------------- +
#region wrap_config_dictConfig() function
@retain_pytest_handlers
def wrap_config_dictConfig(log_config):
    """
    Apply the logging configuration using dictConfig while retaining pytest handlers.
    """
    try:
        # Now invoke the dictConfig function to apply the logging configuration
        logging.config.dictConfig(log_config)
    except Exception as e:
        # Exceptions from dictConfig can be deeply nested. The issues is 
        # most likely with the configuration json itself, not the logging module.
        m = f"Error: logging.config.dictConfig() "
        m += append_cause("", e)
        raise RuntimeError(m) from e
#endregion wrap_config_dictConfig() function
# ---------------------------------------------------------------------------- +
#region validate_file_logging_config() function
def validate_file_logging_config(config_json:dict) -> bool:
    """ Pre-validate the file log config for support and dictConfig() format. 
    """
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
    # TODO: should support check for other p3Logging-supported handlers?
    # Like QueueHandler, QueueListener, etc.
    # Iterate supported file handlers, check log file access
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
    return True
#endregion validate_file_logging_config() function
# ---------------------------------------------------------------------------- +
#region validate_config_file() function
def validate_config_file(config_file:str) -> dict:
    """
    Validate the file contains valid json, return it as a dictionary.
    """
    me = fpfx(validate_config_file)
    global _log_config_path
    # Check if the config file exists, is accessible, and is valid JSON
    if (config_file_path := is_path_reachable(config_file)) is None:
        raise FileNotFoundError(f"Config file not found:'{config_file}'")
    try:
        # Read the config file and parse it as JSON
        with open(config_file_path, "r") as f_in:
            _log_config_path = config_file_path
            config_json = pyjson5.decode_io(f_in)
            return config_json
    except TypeError as e:
        log_exc(validate_config_file, e, print_flag=True)
        t = type(config_file).__name__
        m = f"{me}Error accessing config_file: '{config_file}' as type: '{t}'"
        print(m)
        raise
    except Exception as e:
        log_exc(validate_config_file, e, print_flag=True)
        raise
#endregion validate_config_file() function
# ---------------------------------------------------------------------------- +
#region setup_logging function
def setup_logging(config_file: str = STDOUT_LOG_CONFIG_FILE,
                  start_queue:bool=True, validate_only:bool=False,
                  filenames: dict|None = None) -> dict|None:
    """ Process a configDict-style JSON file to validate and configure logging.

    A valid json file is required. When validate_only is True, the function
    will only validate the json file and return the config_dict. 
    If False (default), the configDict is applied to the logging module.
    
    Args:
        config_file (str): 
            One of the builtin config file names, a relative path to cwd, 
            or an absolute path to a JSON file.
        start_queue (bool): 
            If True, start the queue listener thread.
        validate_only (bool): 
            If True, only validate the config file and return the 
            config_dict without applying it.
        filenames (dict):
            A dictionary of filename values by FileHandler Id keys. If
            a FileHander with the given Id is found in the config file, 
            use the corresponding filename value from the filenames 
            dictionary, overriding the filename entry in the config.
            Use value of None to apply the filename from the config file.
        
    Returns:
        dict|None: The logging configuration dictionary if validate_only is True, 
        otherwise None.
        
    Raises:
        FileNotFoundError: If the config file is not found or not accessible.
        TypeError: If the config file is not a valid JSON file.
        ValueError: If the config file is not a valid logging configuration file.
    """
    try:
        # Config File Preprocessing ------------------------------------------ +
        global _log_config_dict
        # me = fpfx(setup_logging)
        # Validate/parse the json config_file to dict
        log_config_dict = validate_config_file(config_file)
        # For FileHandler types, validate the filenames included in the config
        valid_config_file:bool = validate_file_logging_config(log_config_dict)
        # If filenames mapping dictionary provided, update the log_config_dict
        if filenames is not None and isinstance(filenames, dict):
            update_FileHandler_filenames(log_config_dict, filenames)
        # If validate_only is True, return the config_dict without applying it
        if valid_config_file and validate_only:
            return log_config_dict
        # Config File Prrocessing -------------------------------------------- +
        # Apply the logging configuration preserving any pytest handlers
        wrap_config_dictConfig(log_config_dict)

        # Config File Postprocessing ----------------------------------------- +
        # Save away the active logging config dict for later use
        _log_config_dict = log_config_dict
        # If a 'queue_handler' is used, start the listener thread
        # TODO: loop through config for all QueueHandler instances?
        queue_handler = logging.getHandlerByName("queue_handler")
        if start_queue and queue_handler is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)
        return log_config_dict
    except Exception as e:
        log_exc(setup_logging, e, print_flag=True)
        raise 
#endregion setup_logging function
# ---------------------------------------------------------------------------- +
#region update_FileHanlder_filenams() function
def update_FileHandler_filenames(config_dict:dict, filenames:dict) -> None:  
    """Update the filenames in the config_dict for FileHandler instances.
    
    Apply a set of filename mapping values to any FileHandler instances 
    in the provided confic_dict. The mapping is a dictionary of
    FileHandler Id keys to filename values. The filename values are
    used to update the filename property of the FileHandler instances
    in the config_dict. The mapping is applied to the config_dict,
    modified in place, so the caller can use the modified config_dict.
    Validate the input parameters and raise errors if they are not valid.

    """
    try:
        # Validate the inputs, harshly.
        if (config_dict is None or not isinstance(config_dict, dict) 
            or len(config_dict) == 0):
            raise TypeError(f"Invalid config_dict: type: " 
                            f"'{type(config_dict).__name__}' "
                            f"value = '{str(config_dict)}'")
        if (filenames is None or not isinstance(filenames, dict) 
            or len(filenames) == 0):
            raise TypeError(f"Invalid filenames: {type(filenames).__name__} "
                            f"value = '{str(filenames)}'")
        # Check if the config_dict has a 'handlers' element
        handlers = config_dict.get("handlers", {})
        if not isinstance(handlers, dict) or len(handlers) == 0: return None
        # Update the handlers' filename values from the filenames mapping dict.
        config_dict["handlers"] = {
            handler_id: {
                **handler_config,
                "filename": filenames[handler_id]
            } if handler_id in filenames and handler_config.get("class") == "logging.handlers.RotatingFileHandler" else handler_config
            for handler_id, handler_config in handlers.items()
        }
    except Exception as e:
        log_exc(update_FileHandler_filenames, e, print_flag=True)
        raise
#endregion update_FileHanlder_filenams() function
# ---------------------------------------------------------------------------- +#region start_queue() function
def start_queue() -> None:
    # If the queue_handler is used, start the listener thread
    queue_handler = logging.getHandlerByName("queue_handler")
    if start_queue and queue_handler is not None:
        queue_handler.listener.start()
#endregion start_queue()() function
#region stop_queue() function
def stop_queue() -> None:
    # If the queue_handler is used, start the listener thread
    queue_handler = logging.getHandlerByName("queue_handler")
    if start_queue and queue_handler is not None:
        queue_handler.listener.stop()
#endregion stop_queue() function
# ---------------------------------------------------------------------------- +
#region get_formatter_reference_by_class() function
def get_formatter_id_by_custom_class_name(formatter:logging.Formatter) -> str:
    """
    From the logging config file, lookup a formatter id associated with the 
    given formatter object instance.
    
    This uses the currently logging config json file last loaded by 
    setup_logging() and only searches custom formatter class references
    specified in the dictConfig()-style json config file. 

    Args:
        handler (logging.Handler): The logging handler to get the formatter id for.

    Returns:
        str: The formatter id, which is a key in the formatters dictionary.
    """
    # https://docs.python.org/3/library/logging.config.html#dictionary-schema-details
    # Get the formatter class from the logger's handlers
    global log_config_dict
    fmt_dict = get_configDict()["formatters"] 
    fmt_id_key = [key for key, value in fmt_dict.items() 
                if 'format' in value and value['format'] == formatter._fmt]
    return fmt_id_key
#endregion get_formatter_reference_by_class() function
# ---------------------------------------------------------------------------- +
#region quick_logging_test() function
def quick_logging_test(app_name:str,log_config_file:str,
                       filenames: dict|None = None) -> bool:
    """Quick correctness test of the current logging setup.
    
    Args:
        app_name (str): The name of the application.
        log_config_file (str): The path to the logging configuration file.
        filenames (dict|None): A dictionary of filename values by FileHandler Id keys.
        
    Returns:
        bool: True if the test was successful, False otherwise.
    """
    try:
        pfx = f"{fpfx(quick_logging_test)} "
        if app_name is None or not isinstance(app_name, str) or len(app_name) == 0:
            print(f"{pfx}app_name is required, cannot be '{str(app_name)}'")
            return False
        if log_config_file == FORCE_EXCEPTION:
            # Support a testcase
            raise Exception(FORCE_EXCEPTION_MSG)
        if (log_config_file is None or 
            not isinstance(log_config_file, str) or 
            len(log_config_file) == 0):
            print(f"{pfx}log_config_file is required, "
                  f"cannot be '{str(log_config_file)}'")
            return False
        ancf = f"{app_name}({log_config_file})"
        # Initialize the logger from a logging configuration file.
        setup_logging(log_config_file,filenames=filenames)
        logger = logging.getLogger(ancf)
        ancf = f"[{ancf}]"
        # Log messages at different levels
        logger.debug(f"Message 1/6 - debug message {ancf}")
        logger.info(f"Message 2/6 - info message {ancf}")
        logger.warning(f"Message 3/6 - warning message {ancf}")
        logger.error(f"Message 4/6 - error message {ancf}")
        logger.critical(f"Message 5/6 - critical message {ancf}")
        try:
            1 / 0
        except ZeroDivisionError as e:
            logger.exception(f"Message 6/6 - Exception message: "
                             f"{str(e)} {ancf}")
        return True
    except Exception as e:
        log_exc(quick_logging_test, e, print_flag=True)
        raise
#endregion quick_logging_test()
# ---------------------------------------------------------------------------- +#region get_logger_formatters() function
#region get_Logger_config_info() function
def get_Logger_config_info(log_configDict:dict|None = None, 
                           indent: int = 0) -> str:
    """ Get logging config info obtained from a dict in dictConfig() format.
    
    Navigate through the logging
    Args:
        log_configDict (dict|None): The logging configuration dictionary to use.
        If value of None provided, the current logging configuration is used.
        indent (int): The indentation level for the output.
    
    Returns:
        A str containing the logging configuration information.
        
    raises:
        TypeError: If a parameter is not of the expected type.
        ValueError: If the logging config dict is invalid.
    """
    if log_configDict is not None and not isinstance(log_configDict, dict):
        t = f"type:'{type(log_configDict).__name__}'"
        v = f"value = '{str(log_configDict)}'"
        raise TypeError(f"Invalid log_configDict: {t} {v}")
    if not isinstance(indent, int):
        t = f"type:'{type(indent).__name__}'"
        v = f"value = '{str(indent)}'"
        raise TypeError(f"Invalid indent: {t} {v}")
    me:str = fpfx(get_Logger_config_info)
    version:int = 0
    formatters: dict = {}
    filters: dict = {}
    handlers: dict = {}
    loggers: dict = {}
    formatter_count = 0
    filter_count = 0
    handler_count = 0
    logger_count = 0
    formatter_ids:str = None
    filter_ids:str = None
    handler_ids:str = None
    logger_ids:str = None
    incremental: bool = False
    disable_existing_loggers: bool = False
    pad = indent * " "
    try:
        # Get the current logging configuration
        # if (log_configDict := get_configDict()) is None: return None
        print(pad)
        # If configDict is None, use the current logging configuration
        if log_configDict is None or len(log_configDict) == 0:
            log_configDict = get_configDict()
        if (config_file_path := get_config_path()) is None:
            config_file_name = "unknown"
        else:
            config_file_name = config_file_path.name
        # Gather the info
        version = log_configDict.get("version", 1)
        incremental = log_configDict.get("incremental", False)
        disable_existing_loggers = log_configDict.get("disable_existing_loggers", True)
        formatters = log_configDict.get("formatters", {})
        formatter_count = len(formatters)
        formatter_ids = str([key for key, value in formatters.items()]) if formatter_count > 0 else ""
        filters = log_configDict.get("filters", {})
        filter_count = len(filters)
        filter_ids = str([key for key, value in filters.items()]) if filter_count > 0 else ""
        handlers = log_configDict.get("handlers", {})
        handler_count = len(handlers)
        handler_ids = str([key for key, value in handlers.items()]) if handler_count > 0 else ""
        loggers = log_configDict.get("loggers", {})
        logger_count = len(loggers)
        logger_ids = str([key for key, value in loggers.items()]) if logger_count > 0 else ""
        root_config_info = get_Logger_root_config_info(log_configDict.get("root", None))

        # Construct summary of the current logging configuration
        m = f"{pad}Logging config({config_file_name}) version({version}) "
        t = f"{formatter_ids}" if formatter_count > 0 else ""
        m = f"formatters({formatter_count}){t} "
        t = f"{filter_ids}" if filter_count > 0 else ""
        m += f"filters({filter_count}){t} " 
        t = f"{handler_ids}" if handler_count > 0 else ""
        m += f"handlers({handler_count}){t} "
        t = f"{logger_ids}" if logger_count > 0 else ""
        m += f"loggers({logger_count}){t} "
        m += f"root config[{root_config_info}]" if root_config_info else ""
        return m
    except Exception as e:
        m = log_exc(get_Logger_config_info, e, print_flag = True)
        raise
#endregion get_Logger_config_info() function
# ---------------------------------------------------------------------------- +
#region get_Logger_root_config_info() function
def get_Logger_root_config_info(root_log_configDict:dict|None = None) -> str:
    """ Get logging config info from 'root' element dict.
    
    The 'root' element of a logging configuration dict is similar to the 
    configDict format, but cannot contain a 'root' element itself. Also,
    the values for 'Formatters', 'Filters', 'Handlers' and 'Loggers' are Lists
    of the IDs used in the higher elements, not dict objects.
    
    Args:
        root_log_configDict (dict|None): The 'root' element dict from a valid
        logging configuration dictionary to use. A value of None returns the 
        empty string, no dict, empty result. 
        
    Returns:
        A str, maybe empty, containing an overview of the 'root' element 
        logging configuration information.
        
    Raises:
        TypeError: If the input is not a dict.
        ValueError: If the input dict is found to have a 'root'
        element, which is invalid.
    """
    if root_log_configDict is None or (): return ""
    if root_log_configDict is not None and not isinstance(root_log_configDict, dict):
        t = f"type:'{type(root_log_configDict).__name__}'"
        v = f"value = '{str(root_log_configDict)}'"
        m = f"Invalid root_log_configDict: {t} {v}"
        raise TypeError(m)
    me:str = fpfx(get_Logger_root_config_info)
    formatters: List = []
    filters: List = []
    handlers: List = []
    loggers: List = []
    formatter_ids: str = ""
    filter_ids: str = ""
    handler_ids: str = ""
    logger_ids: str = ""
    formatter_count = 0
    filter_count = 0
    handler_count = 0
    logger_count = 0
    try:
        # Get the current logging configuration
        # Gather the info
        if "root" in root_log_configDict:
            m = f"{me} Invalid: root Logging config({root_log_configDict}) "
            m += "contains 'root' element"
            print(m)
            raise ValueError(m)
        if "formatters" in root_log_configDict:
            formatters = root_log_configDict["formatters"]
            formatter_count = len(formatters)
            formatter_ids = str(formatters) if formatter_count > 0 else ""
        if "filters" in root_log_configDict:
            filters = root_log_configDict["filters"]
            filter_count = len(filters)
            filter_ids = str(filters) if filter_count > 0 else ""
        if "handlers" in root_log_configDict:
            handlers = root_log_configDict["handlers"]
            handler_count = len(handlers)
            handler_ids = str(handlers) if handler_count > 0 else ""
        if "loggers" in root_log_configDict:
            loggers = root_log_configDict["loggers"]
            logger_count = len(loggers) 
            logger_ids = str(loggers) if logger_count > 0 else ""
        # Construct summary of the root logging configuration
        m = f"root config[ "
        m += f"formatters({formatter_count}){formatter_ids} "
        m += f"filters({filter_count}){filter_ids} " 
        m += f"handlers({handler_count}){handler_ids} "
        m += f"loggers({logger_count}){logger_ids} ]"
        return m
    except Exception as e:
        m = log_exc(get_Logger_config_info, e, print_flag = True)
        raise
#endregion get_Logger_root_config_info() function
# ---------------------------------------------------------------------------- +
#region get_logger_formatters() function
def get_logger_formatters(
    handler_param: logging.Handler | List[logging.Handler]) -> List[logging.Formatter]:
    """Collect Formatter objs from an instance or List of logging.Handler objs.
    
    Args:
        handler_param (logging.Handler | List[logging.Handler]): A single
        instance or List of logging.Handler objects.
        
    Returns:
        List[logging.Formatter]: A list of logging.Formatter objects.
        
    Raises:
        TypeError: If the handler is not a logging.Handler or a list of 
        logging.Handler objects.
    """
    me = fpfx(get_logger_formatters)
    #region param 'handler_param' type check
    raise_TypeError = False
    # Must be a single instance, list or tuple of logging.Handler objects
    # After validation, handlers will be a List of one or more logging.Handler
    # objects.
    if handler_param is None:raise_TypeError = True
    elif isinstance(handler_param, logging.Handler): handlers = [handler_param]
    elif ((isinstance(handler_param, List) or isinstance(handler_param, tuple)) 
        and all(isinstance(obj, logging.Handler) for obj in handler_param)):
        handlers = handler_param
    else:
        raise_TypeError = True
    if raise_TypeError:
        m = str(
            f"param 'handler_param' is type:'{type(handler_param).__name__}', "
            f"value is '{handler_param}', "
            f"expected one or List of logging.Handler objects."
        )
        print(f"{me}{m}")
        raise TypeError(m)
    #endregion param 'handler_param' type check
    try:
        # Navigate the handlers to collect info on the configured formatters.
        formatters = []
        for handler in handlers:
            if isinstance(handler, logging.StreamHandler):
                formatter = handler.formatter
                formatters.append(formatter) if formatter else None
            elif isinstance(handler, logging.FileHandler):
                formatter = handler.formatter
                formatters.append(formatter) if formatter else None
            # logging.handlers.QueueHandler
            elif isinstance(handler, logging.handlers.QueueHandler):
                # A listener has a list of handlers, collect them if present.
                listener = handler.listener
                hl = listener.handlers if listener else None
                formatters += get_logger_formatters(hl) if hl else None
        return formatters
    except Exception as e:
        print(log_exc(get_logger_formatters, e, print_flag=True))
        raise
#endregion get_logger_formatters() function
# ---------------------------------------------------------------------------- +
