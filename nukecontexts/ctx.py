import sys
from contextlib import contextmanager


class NukeContextError(ValueError):
    def __init__(self, message, *args):
        self.message = message
        super(NukeContextError, self).__init__(message, *args)


@contextmanager
def enabled(nodes, verbose=False):
    """
    Given a list of nodes (:class:`~nuke.Node`), enable on entry and restore
    to original value on exit.

    :param nodes: Nodes
    :type nodes: list
    :param verbose: Print attribute changes to stdout
    :type verbose: bool
    """
    with set_attr(nodes, 'disable', False, verbose=verbose):
        yield


@contextmanager
def disabled(nodes, verbose=False):
    """
    Given a list of nodes (:class:`~nuke.Node`), disable on entry and restore
    to original value on exit.

    :param nodes: Nodes
    :type nodes: list
    :param verbose: Print attribute changes to stdout
    :type verbose: bool
    """
    with set_attr(nodes, 'disable', True, verbose=verbose):
        yield


@contextmanager
def set_attr(nodes, attr, value, verbose=False):
    """
    Given a list of nodes (:class:`~nuke.Node`), set a given ``attr`` to
    ``value`` entry and restore to original value on exit.

    :param nodes: Nodes
    :type nodes: list
    :param attr: Attribute
    :type attr: str
    :param value: Value
    :type value: str, int, float, bool
    :param verbose: Print attribute changes to stdout
    :type verbose: bool
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
            raise NukeContextError('Node \'{0}\': {1}'.format(node.name(), err.args[0]))
        if verbose:
            print 'Setting attribute \'{0}\' on node \'{1}\' to value \'{2}\''.format(attr, node.name(), value)
        try:
            node[attr].setValue(value)
        except TypeError as err:
            raise NukeContextError('Attribute \'{0}\': {1}'.format(attr, err.args[0]))
    try:
        yield
    finally:
        for node, enter_value in enter_values.iteritems():
            if verbose:
                print 'Restoring attribute \'{0}\' on node \'{1}\' to value \'{2}\''.format(attr, node.name(), enter_value)
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
