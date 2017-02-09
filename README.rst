nukecontexts
============

nukecontexts is a library of composable context managers for Nuke to manage the state of complex compositing scripts in code.

The most common use case for nukecontexts is automated rendering of multiple states of a compositing script. For example two different outputs, jpg and png.::

    import nuke
    from nukecontexts import ctx

    node = nuke.toNode('render_node')
    with ctx.set_attr(node, 'file_type', 'jpeg'):
        nuke.execute(node.name(), 1, 1, 1)
    with ctx.set_attr(node, 'file_type', 'png'):
        nuke.execute(node.name(), 1, 1, 1)

The real power of nukecontexts comes with composable contexts, using ``multiple_contexts``. ::

    merge_node = nuke.toNode('Merge1')
    grade_node = nuke.toNode('Grade1')
    switch_node = nuke.toNode('Switch1')

    ctx1 = ctx.enable([merge_node, grade_node])
    ctx2 = ctx.set_attr(grade_node, 'gain', 2.0)
    ctx3 = ctx.set_attr(switch_node, 'which', 0)

    with ctx.multiple_contexts([ctx1, ctx2, ctx3]):
        # Render with the grade node's gain attribute set to 2.0
        nuke.execute(node.name(), 1, 1, 1)

    with ctx.multiple_contexts([ctx1, ctx3]):
        # Render with the grade node's gain attribute set to the original value
        nuke.execute(node.name(), 1, 1, 1)
