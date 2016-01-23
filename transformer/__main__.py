import os
import sys

# insert the root dir into the system path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from transformer.app import app, serve_locally
serve_locally(app)
