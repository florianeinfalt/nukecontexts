import os
import re
import sys
import platform

try:
    os.environ['DOCS_CONTEXT']
except:
    if platform.system() == 'Darwin':
        application = r'Nuke\d+\.\d+v\d+.app'
    elif platform.system() == 'Windows':
        application = r'Nuke\d+\.\d+.exe'
    else:
        raise RuntimeError('OS {0} is not supported'.format(platform.system()))

    match = re.search(application, sys.executable)
    if not match:
        raise RuntimeError('Import nukecontexts from within Nuke')

__version__ = '0.1.2'
__all__ = ['ctx']

from ctx import enabled, disabled, set_attr, multiple_contexts
