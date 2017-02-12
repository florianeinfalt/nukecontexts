import nuke
import pytest

@pytest.fixture(scope='session')
def node():
    return nuke.nodes.Write(name='test_write')
