import json
import os
import pickle
import pprint
import re
import socket
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import main

data = {}

data = main.accept_data()
print(f"{data}")
