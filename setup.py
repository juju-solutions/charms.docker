import os
from setuptools import setup

version_file = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'VERSION'))

with open(version_file) as v:
    VERSION = v.read().strip()



setup(
    name = "charms.docker",
    version = VERSION,
    author = "Charles Butler",
    author_email = "charles.butler@ubuntu.com",
    url = "http://github.com/juju-solutions/charms.docker",
    description = ( "Python wrappers for the docker CLI and configuring the Docker Daemon in Juju Charms" ),
    license = "GPLv3",
    keywords = "docker juju charm charms",
    packages = ['charms.docker'],
    long_description = "",
    classifiers = [
        "Development Status :: 3 - Alpha",
    ],
)
