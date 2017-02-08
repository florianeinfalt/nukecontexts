import sys
from contextlib import contextmanager


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
    if not isinstance(nodes, list):
        nodes = [nodes]
    enter_values = {}
    for node in nodes:
        enter_values[node] = node['disable'].value()
        if verbose:
            print 'Enabling node: {0}'.format(node.name())
        node['disable'].setValue(False)
    try:
        yield
    finally:
        for node, enter_value in enter_values.iteritems():
            if verbose:
                print 'Restoring node: {0}'.format(node.name())
            node['disable'].setValue(enter_value)


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
    if not isinstance(nodes, list):
        nodes = [nodes]
    enter_values = {}
    for node in nodes:
        enter_values[node] = node['disable'].value()
        if verbose:
            print 'Disabling node: {0}'.format(node.name())
        node['disable'].setValue(True)
    try:
        yield
    finally:
        for node, enter_value in enter_values.iteritems():
            if verbose:
                print 'Restoring node: {0}'.format(node.name())
            node['disable'].setValue(enter_value)


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
