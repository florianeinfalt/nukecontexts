import os
import pytest

dir_ = os.path.dirname(__file__)
pytest.main(['{0}/tests/'.format(dir_), '--cov=nukecontexts', '--cov-report', 'term-missing'])
