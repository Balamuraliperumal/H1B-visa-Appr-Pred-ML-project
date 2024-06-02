import logging
import os
from datetime import datetime
from from_root import from_root

log_file=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_dir="logs"

logs_path=os.path.join(from_root(),log_dir,log_file)

os.makedirs(log_dir,exist_ok=True)

logging.basicConfig(
    filename=logs_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level = logging.DEBUG,
)
