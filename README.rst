nukecontexts
============

.. image:: https://img.shields.io/pypi/l/nukecontexts.svg
    :target: https://pypi.python.org/pypi/nukecontexts
.. image:: https://img.shields.io/pypi/pyversions/nukecontexts.svg
    :target: https://pypi.python.org/pypi/nukecontexts
.. image:: https://img.shields.io/pypi/v/nukecontexts.svg
    :target: https://pypi.python.org/pypi/nukecontexts
.. image:: https://img.shields.io/pypi/wheel/nukecontexts.svg
    :target: https://pypi.python.org/pypi/nukecontexts
.. image:: https://readthedocs.org/projects/nukecontexts/badge/?version=latest
    :target: https://readthedocs.org/projects/nukecontexts/?badge=latest

``nukecontexts`` is a library of composable context managers for Nuke to manage the state of complex compositing scripts in code.

`Full Documentation`_

Installation
------------

To install ``nukecontexts``, type:

.. code-block:: bash

    $ pip install nukecontexts


Open Nuke's ``init.py`` file and add: ::

    nuke.pluginAddPath('/path/to/your/local/python/site-packages')

Getting Started
---------------

The most common use case for ``nukecontexts`` is automated rendering of multiple states of a compositing script. For example two different output formats, jpg and png.

.. code:: python

    import nuke
    from nukecontexts import ctx

    render_node = nuke.toNode('Write1')
    with ctx.set_attr(render_node, 'file_type', 'jpeg'):
        nuke.execute(render_node.name(), 1, 1, 1)
    with ctx.set_attr(render_node, 'file_type', 'png'):
        nuke.execute(render_node.name(), 1, 1, 1)

The power of ``nukecontexts`` comes with composable contexts, using ``multiple_contexts()``. Arbitrarily complex, varying states of the compositing script can be defined and used to automatically generate different results.

.. code:: python

    merge_node = nuke.toNode('Merge1')
    grade_node = nuke.toNode('Grade1')
    switch_node = nuke.toNode('Switch1')

    ctx1 = ctx.enable([merge_node, grade_node])
    ctx2 = ctx.set_attr(grade_node, 'white', 2.0)
    ctx3 = ctx.set_attr(switch_node, 'which', 0)
    ctx4 = ctx.disable(merge_node)

    with ctx.multiple_contexts([ctx1, ctx2, ctx3]):
        """Render with the merge_node and grade_node enabled, the
        grade_node's white attribute set to 2.0 and the switch_node's switch
        position set to 0."""
        nuke.execute(render_node.name(), 1, 1, 1)

    with ctx.multiple_contexts([ctx3, ctx4]):
        """Render with the switch_node's switch position set to 0 and the
        merge node disabled; the grade_node's gain value remains at the
        original value."""
        nuke.execute(render_node.name(), 1, 1, 1)

.. _Full Documentation: http://nukecontexts.readthedocs.io/en/latest/
