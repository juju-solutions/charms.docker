Installation
------------

charms.docker is available via pip. For source packages, see `GitHub`_.

Pip
~~~~~~

Ideally you will do this in a virtualenv, and are familiar with working
with the virtualenv package.

.. code:: bash

    pip install charms.docker

Source
~~~~~~

charms.docker is built with Python3, so please make sure it’s installed prior
to following these steps.

To install charms.docker from source, first get the source:

.. code:: bash

    git clone https://github.com/juju-solutions/charms.docker.git

Move in to the ``charms.docker`` directory and run:

.. code:: bash

     sudo python3 setup.py install

     You can also access the Python libraries; however, your ``PYTHONPATH``
     will need to be amended in order for it to find the charms.docker directory.

.. _GitHub: https://github.com/juju-solutions/charms.docker/releases
