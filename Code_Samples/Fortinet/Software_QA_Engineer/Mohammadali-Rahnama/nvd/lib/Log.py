import logging
import os

def setup_log(log_file_path, log_file_name, logger_name):
    # Create logs directory if it doesn't exist
    log_dir = str(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, f"{log_file_name}.log")),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(logger_name)

    return logger
