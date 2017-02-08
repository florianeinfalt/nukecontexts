import re
import sys

match = re.search(r'Nuke\d+\.\d+.exe', sys.executable)
if not match:
    raise RuntimeError('Import nukecontexts from within Nuke')

__version__ = '0.1'
