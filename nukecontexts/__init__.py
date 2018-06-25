import os
import re
import sys
import getpass
import logging
import platform


def import_nuke():
    try:
        import nuke
        return nuke
    except ImportError as e:
        try:
            os.environ['NON_PRODUCTION_CONTEXT']
        except KeyError:
            raise e


TESTING = False
try:
    TESTING = os.environ['NON_PRODUCTION_CONTEXT']
    logger = logging.getLogger()
    sentry = None
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
    nuke = import_nuke()

__version__ = '0.2.0'
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


def get_sentry():
    try:
        from raven import Client
        try:
            os.environ['SENTRY_DSN']
        except KeyError:
            raise ImportError
        client = Client(release=__version__)
        client.user_context({'username': getpass.getuser()})
        client.tags_context({
                'os_version': platform.platform(),
                'nuke_version': nuke.NUKE_VERSION_STRING})
        return client
    except ImportError:
        return None


if not TESTING:
    logger = create_logger()
    sentry = get_sentry()
