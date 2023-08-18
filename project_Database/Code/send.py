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

data = {"1": "a", "2": "b", "3": "c"}

main.send_data(data)
