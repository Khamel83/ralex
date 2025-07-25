import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

print("sys.path:", sys.path)

if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = 'tests/unit'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)