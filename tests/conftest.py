import nuke
import pytest

@pytest.fixture(scope='session')
def nuke():
    import nuke
    return nuke

@pytest.fixture(scope='session')
def node(nuke):
    return nuke.nodes.Write(name='test_write')
