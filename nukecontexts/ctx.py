import sys
from contextlib import contextmanager

from tqdm import tqdm

from nukecontexts import logger
from nukecontexts import sentry


class NukeContextError(ValueError):
    def __init__(self, message, *args):
        self.message = message
        super(NukeContextError, self).__init__(message, *args)


class Progress(object):
    """
    Convenience wrapper class around :func:`tqdm.tqdm` for easy progress bars

    Usage:

    >>> with Progress(iterable) as progress:
    >>>    for item in progress:
    >>>        #do something
    """
    def __init__(self, iterable, name='nukecontexts', output=sys.stdout):
        """
        :param interable: Iterable to generate progress bar for
        :type interable: iter
        :param name: Progress bar label (default: 'nukecontexts')
        :type name: str
        :param output: Output stream (default: ``sys.stdout``)
        :type output: io.TextIOWrapper or io.StringIO
        """
        self.name = name
        self.iterable = iterable
        self.output = output

    def __enter__(self):
        """
        :return: Progress bar
        :rtype: tqdm.tqdm
        """
        return tqdm(iterable=self.iterable,
                    desc=self.name,
                    file=self.output)

    def __exit__(self, type, value, traceback):
        pass


@contextmanager
def enabled(nodes, log=logger):
    """
    Given a list of nodes (:class:`~nuke.Node`), enable on entry and restore
    to original value on exit.

    :param nodes: Nodes
    :type nodes: list
    :param log: Logger
    :type log: logging.Logger
    """
    with set_attr(nodes, 'disable', False, log=log):
        yield


@contextmanager
def disabled(nodes, log=logger):
    """
    Given a list of nodes (:class:`~nuke.Node`), disable on entry and restore
    to original value on exit.

    :param nodes: Nodes
    :type nodes: list
    :param log: Logger
    :type log: logging.Logger
    """
    with set_attr(nodes, 'disable', True, log=log):
        yield


@contextmanager
def set_attr(nodes, attr, value, log=logger):
    """
    Given a list of nodes (:class:`~nuke.Node`), set a given ``attr`` to
    ``value`` entry and restore to original value on exit.

    :param nodes: Nodes
    :type nodes: list
    :param attr: Attribute
    :type attr: str
    :param value: Value
    :type value: str, int, float, bool
    :param log: Logger
    :type log: logging.Logger
    """
    if not isinstance(nodes, list):
        nodes = [nodes]
    enter_values = {}
    for node in nodes:
        try:
            assert node
        except AssertionError:
            raise NukeContextError('Invalid node')
        try:
            enter_values[node] = node[attr].value()
        except NameError as err:
            raise NukeContextError('Node \'{0}\': {1}'.format(node.name(),
                                                              err.args[0]))
        logger.info('Entering context: ({0}/{1}/{2})'.format(node.name(),
                                                             attr,
                                                             value))
        try:
            node[attr].setValue(value)
        except TypeError as err:
            raise NukeContextError('Attribute \'{0}\': {1}'.format(attr, err.args[0]))
    try:
        yield
    finally:
        for node, enter_value in enter_values.iteritems():
            logger.info('Restoring context: ({0}/{1}/{2})'.format(node.name(),
                                                                  attr,
                                                                  enter_value))
            node[attr].setValue(enter_value)


@contextmanager
def multiple_contexts(contexts):
    """
    Given a list of contextmanagers, sequentially enter all contextmanagers,
    raise :class:`Exception` in case errors occur in contexts.

    :param contexts: List of contextmanagers
    :type contexts: list
    """
    for ctx in contexts:
        ctx.__enter__()

    err = None
    exc_info = (None, None, None)
    try:
        yield
    except Exception as err:
        exc_info = sys.exc_info()

    # exc_info gets passed to each subsequent ctx.__exit__
    # unless one of them suppresses the exception by returning True
    for ctx in reversed(contexts):
        if ctx.__exit__(*exc_info):
            err = False
            exc_info = (None, None, None)
    if err:
        raise err
