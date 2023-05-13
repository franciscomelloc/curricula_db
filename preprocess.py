from pathlib import Path
import numpy as np
import pandas as pd

from utils import *

#.venv\Scripts\activate

BASE_DIR = Path().absolute() # Document path
DATA_DIR = BASE_DIR / 'data' # Path to data

df = utils.read_docs_paragraph(DATA_DIR)
