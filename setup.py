from setuptools import setup

setup(
    name = "charms.docker",
    version = '0.1.8',
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
