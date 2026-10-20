import os
import sys

# Tambahkan root direktori ke sys.path agar modul app dan src dapat di-import oleh serverless handler
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app
