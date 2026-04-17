import sys
import os

# Make goal_tracker package importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'goal_tracker'))

from main import app
