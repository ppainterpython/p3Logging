
import p3Logging as p3l

if __name__ == "__main__":
    try:
        # Apply the logging configuration from config_file
        p3l.setup_logging(p3l.STDOUT_LOG_CONFIG_FILE,start_queue=False)
        m = p3l.get_logger_info()
        print(m)
        # show_logging_setup()
    except Exception as e:
        print(str(e))
        exit(1)
