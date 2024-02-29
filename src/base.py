'''
    头文件
'''
import requests
import json
import sys
import time
import copy
import logging
import math
import re
import os
from array import array
import numpy as np
from scipy.spatial.transform import Rotation

logging.basicConfig(filename='/data/home/user/workspace/python_unit_test/log/robot_unit.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('my_logger')
file_handler = logging.FileHandler('/data/home/user/workspace/robotics_python/log/robot_unit.logger')

console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)