import os

from typing import Tuple

def_figsize: Tuple = (14, 7)

ROOT_DIR: str = os.path.abspath(os.pardir)

csv_path: str = f'{ROOT_DIR}/data/deviation.csv'
json_path: str = f'{ROOT_DIR}/data/deviation.json'
url_path: str = f'{ROOT_DIR}/https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
