# Charms.Docker

This is a library intended to ease development of docker
deliverable charms, by exposing an API that is easy to
grok at an initial glance.

This library was borne from a disgust of mine at seeing many
`subprocess.check_call` lines littered throughout charms.
While functionally similar to what this library exposes, it
should read better than many disjointed os exec calls.

### To use charms.docker

This is actually embedded in the [`layer:docker`](http://interfaces.juju.solutions)
runtime layer. Unless you intend on hacking this, porting it elsewhere, or otherwise
distrust the layer - you wont need to manually install this.

#### Examples

Launch a container

	from charms.docker import Docker
        d = Docker()
        pid = d.up('lazypower/idlerpg:latest', dirs={"files/idlerpg":"/files/idlerpg"}, ports=["8000:8000"])
	payload-register('docker', 'application', pid)
