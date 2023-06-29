import sys
import os
from dotenv import load_dotenv

load_dotenv()

SRC_PATH = os.getenv('SRC_PATH')
REGEX_PATH = os.getenv('REGEX_PATH')


sys.path.append(SRC_PATH)
sys.path.append(REGEX_PATH)