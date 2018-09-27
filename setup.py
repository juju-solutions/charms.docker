from setuptools import setup

with open('README.md') as fp:
    long_desc = fp.read()

setup(
    name="charms.docker",
    version='0.1.19',
    author="Charles Butler",
    author_email="charles.butler@ubuntu.com",
    url="http://github.com/juju-solutions/charms.docker",
    description=("Python wrappers for the docker CLI and configuring the "
                 "Docker Daemon in Juju Charms"),
    long_description_content_type="text/markdown",
    long_description=long_desc,
    license="GPLv3",
    keywords="docker juju charm charms",
    packages=['charms.docker'],
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
)
