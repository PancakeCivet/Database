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
from main import Filed, FiledType, Table_struct

Table_dict: dict[str, Table_struct] = {}

print(Table_dict)