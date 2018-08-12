import os
import sys

# only apply hack if we're not running a specialized test
if 'tests' not in os.getcwd():
    os.chdir('./tests/')
    sys.path.append('../src/')
