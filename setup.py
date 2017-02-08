from setuptools import setup, find_packages

setup(
    name = 'nukecontexts',
    version = '0.1',
    description='Library of composable context managers for Nuke',
    url='http://www.florianeinfalt.de',
    author='Florian Einfalt',
    author_email='info@florianeinfalt.de',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
