import logging
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent.parent
LOG_DIR=BASE_DIR/"logs"

LOG_DIR.mkdir(exist_ok=True)

LOG_FILE=LOG_DIR/"dashboard.log"

def get_logger():
    logger=logging.getLogger("healthcare_dashboard")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        formatter=logging.Formatter(
            "%(asctime)s|%(levelname)s|%(message)s"
        )
        
        file_handler=logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        )
        
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        
    logger.propagate=False
    
    return logger