import os
import logging

def setup_logger(log_file: str = "logs/pipeline.log") -> logging.Logger:
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger("MotorInsurancePipeline")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

def log_pipeline_step(message: str):
    logger = setup_logger()
    logger.info(message)

def log_error(message: str):
    logger = setup_logger()
    logger.error(message)
