# Charms.Docker

[![Build Status](https://travis-ci.org/juju-solutions/charms.docker.svg?branch=master)](https://travis-ci.org/juju-solutions/charms.docker) [![Coverage Status](https://coveralls.io/repos/github/juju-solutions/charms.docker/badge.svg?branch=master)](https://coveralls.io/github/juju-solutions/charms.docker?branch=master)

This is a library intended to ease development of docker
deliverable charms, by exposing an API that is easy to
grok at an initial glance.

This library was borne from a disgust of mine at seeing many
`subprocess.check_call` lines littered throughout charms.
While functionally similar to what this library exposes, it
should read better than many disjointed os exec calls.

This library is also targeted at python 3.3+

## To use charms.docker

This is actually embedded in the [`layer:docker`](http://github.com/juju-solutions/layer-docker)
runtime layer. Unless you intend on hacking this, porting it elsewhere, or otherwise
distrust the layer - you wont need to manually install this.

### Examples

#### Launch a one-off container

	from charms.docker import Docker
        d = Docker()
        pid = d.up('lazypower/idlerpg:latest', dirs={"files/idlerpg":"/files/idlerpg"}, ports=["8000:8000"])
	payload-register('docker', 'application', pid)


#### Launch a configured container, or many containers

But you wouldn't really want to use this terribly often, as its more sensible
to encapsulate the "configured state" of the container via a docker-compose yaml.
Which is rumored to be simple to template, and then be used like so assuming the
rendered template resides in `$CHARM_DIR/files/workspace/docker-compose.yml`:

	from charms.docker import Compose
	c = Compose('files/workspace')
	c.up()

### Get support

This project is under heavy development pending a 0.1.0 release. Until such time
no methods should be assumed to be concrete until we land on a 1.0.0 release
chain. Any charms based on this will be at the mercy of the author to stay abreast
of the charm libraries changes.

- **Issue Tracker**: [http://github.com/juju-solutions/charms.docker/issues](http://github.com/juju-solutions/charms.docker/issues)
- **Juju Mailing List**: [juju@lists.ubuntu.com](mailto:juju@lists.ubuntu.com)
