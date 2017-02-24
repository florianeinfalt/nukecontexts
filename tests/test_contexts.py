import pytest
from nukecontexts import ctx


def test_enabled(node):
    node['disable'].setValue(True)
    assert node['disable'].value()
    with ctx.enabled(node):
        assert not node['disable'].value()
    assert node['disable'].value()
    node['disable'].setValue(False)


def test_disabled(node):
    assert not node['disable'].value()
    with ctx.disabled(node):
        assert node['disable'].value()
    assert not node['disable'].value()


def test_set_attr_errors(node):
    # Test invalid node error
    with pytest.raises(ctx.NukeContextError):
        with ctx.set_attr(None, 'invalid_attr', True):
            print 'should not print'
    # Test invalid attribute error
    with pytest.raises(ctx.NukeContextError):
        with ctx.set_attr(node, 'invalid_attr', True):
            print 'should not print'
    # Test invalid value error
    with pytest.raises(ctx.NukeContextError):
        with ctx.set_attr(node, 'file_type', 2.0):
            print 'should not print'


def test_multiple(node):
    ctx1 = ctx.enabled(node)
    ctx2 = ctx.set_attr(node, 'file_type', 'jpeg')
    ctx3 = ctx.set_attr(node, 'channels', 'rgba')

    node['disable'].setValue(True)
    node['file_type'].setValue('exr')

    assert node['disable'].value()
    assert node['file_type'].value() == 'exr'
    assert node['channels'].value() == 'rgb'

    with ctx.multiple_contexts([ctx1, ctx2, ctx3]):
        assert not node['disable'].value()
        assert node['file_type'].value() == 'jpeg'
        assert node['channels'].value() == 'rgba'

    assert node['disable'].value()
    assert node['file_type'].value() == 'exr'
    assert node['channels'].value() == 'rgb'

    node['disable'].setValue(False)


def test_progress(node):
    ctx1 = ctx.enabled(node)
    iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    with ctx1, ctx.Progress(iterable) as progress:
        for idx, item in enumerate(progress):
            assert item == idx + 1


def test_inventory(nuke):
    with ctx.inventory('new_nodes'):
        for i in range(3):
            nuke.createNode('Write', inpanel=False)
    assert len(new_nodes) == 3
    assert any([node for node in new_nodes if node.Class() == 'Write'])
