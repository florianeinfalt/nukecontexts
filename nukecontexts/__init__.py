import os
import re
import sys
import logging
import platform

try:
    os.environ['NON_PRODUCTION_CONTEXT']
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


def create_logger():
    logger = logging.getLogger(__name__)
    logger.handlers = []
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(fmt='%(asctime)s: %(name)s: '
                                      '%(levelname)s: %(message)s',
                                  datefmt='%d/%m/%Y %I:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


logger = create_logger()
