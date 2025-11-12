import os
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


list_of_files = [
    "src/__init__.py",
    "src/graphs/__init__.py",
    "src/llms/__init__.py",
    "src/nodes/__init__.py",
    "src/states/__init__.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    
    # create directory if doesn't exist
    if not os.path.exists(filedir):
        logging.info(f"{filedir} doesn't exist creating...")
        os.makedirs(filedir)
    
    # create files
    if not os.path.exists(filepath):
        logging.info(f"{filepath} doesn't exist creating one...")
        with open(filepath, "wb"):
            # left empty on purpose
            pass
        
    else:
        logging.info(f"{filepath} already exists.")