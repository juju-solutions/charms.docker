import os
import subprocess

from shlex import split
from .workspace import Workspace


class Docker:
    '''
    Wrapper class to communicate with the Docker daemon on behalf of
    a charmer. Provides stateless operations of a running docker daemon
    '''

    def __init__(self, socket="unix:///var/run/docker.sock", workspace=None):
        '''
        :param socket: URI to the Docker daemon socket
            default: unix:///var/run/docker.sock

        :param workspace: Path to directory containing a Dockerfile
            default: None
        '''
        self.socket = socket
        if workspace:
            self.workspace = Workspace(workspace)

    def login(self, user, password, email, registry=None):
        '''
        Docker login exposed as a method.

        :param user:  Username in the registry
        :param password: - Password for the registry
        :param email: - Email address on account (dockerhub)
        '''
        cmd = "login -u {0} -p {1} -e {2}".format(user, password, email)
        if registry:
            cmd = "{0} {1}".format(cmd, registry)
        return self._run(cmd)

    def logs(self, container_id):
        '''
        Docker logs exposed as a method.

        :param container_id: - UUID for the container to fetch logs
        '''
        cmd = "logs {}".format(container_id)
        return self._run_with_output(cmd)

    def kill(self, container_id):
        ''' Kill a running container '''
        cmd = "kill {}".format(container_id)
        return self._run(cmd)

    def pedantic_kill(self, container_id):
        ''' Pedantically kill a container, by killing it, then wait, then
            rm -rf it.'''

        # a workaround for bug https://github.com/docker/docker/issues/3968.
        out = self.kill(container_id)
        if out != 0:
            print("Failed killing container")

        out = self.wait(container_id)
        if out != 0:
            print("Failed waiting on container")

        return self.rm(container_id, True, True)

    def ps(self):
        '''
        return a string of docker status output
        '''
        cmd = "ps"
        return self._run_with_output(cmd)

    def pull(self, image):
        '''
        Pull an image from the docker hub
        '''
        cmd = "pull {}".format(image)
        return self._run_with_output(cmd)

    def rm(self, container_id, force=False, volume=False):
        cmd = "rm"
        if force:
            cmd = "{0} {1}".format(cmd, "-f")
        if volume:
            cmd = "{0} {1}".format(cmd, "-v")

        cmd = "{0} {1}".format(cmd, container_id)

        return self._run(cmd)

    def run(self, image, options=[], commands=[], arg=[]):
        '''
        Docker Run exposed as a method. This wont be as natural as the
        command line docker experience.

        Docker CLI output example:
        Usage:	docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

        :param image: string of the container to pull from the registry,
                        eg: ubuntu:latest
        :param options:  array of string  options, eg: ['-d', '-v /tmp:/tmp']
        :param commands:  array of string commands, eg: ['ls']
        :param arg:  array of string command args, eg: ['-al']
        '''
        options = ' '.join(options)
        command = ' '.join(commands)
        args = ' '.join(arg)
        cmd = "run {0} {1} {2} {3}".format(
            options, image, command, args)
        return self._run_with_output(cmd)
        # try:
        #     subprocess.check_output(split(cmd))
        # except subprocess.CalledProcessError as expect:
        #     print("Error: ", expect.returncode, expect.output)

    def running(self):
        '''
        Predicate method to determine if the daemon we are talking to is
        actually online and recieving events.

        ex: bootstrap = Docker(socket="unix:///var/run/docker-boostrap.sock")
        bootstrap.running()
        > True
        '''
        # TODO: Add TCP:// support for running check
        return os.path.isfile(self.socket)

    def wait(self, container_id):
        ''' Block until a container has successfully stopped, and returns the
            exit code '''
        cmd = "wait {}".format(container_id)
        return self._run(cmd)

    def _run(self, cmd):
        ''' Abstracted run commands that returns only the response code'''
        if self.socket:
            cmd = "docker -H {} {}".format(self.socket, cmd)
        else:
            cmd = "docker {}".format(cmd)

        try:
            return subprocess.check_call(split(cmd))
        except subprocess.CalledProcessError as expect:
            print("Error: ", expect.returncode, expect.output)
            return 1

    def _run_with_output(self, cmd):
        ''' Abstracted run commands that return text output '''

        if self.socket:
            cmd = "docker -H {} {}".format(self.socket, cmd)
        else:
            cmd = "docker {}".format(cmd)

        try:
            return subprocess.check_output(split(cmd)).decode('ascii')
        except subprocess.CalledProcessError as expect:
            return "Error: {}, {}".format(expect.returncode, expect.output)
