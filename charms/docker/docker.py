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
        cmd = "docker run {0} {1} {2} {3}".format(
            options, image, command, args)

        try:
            subprocess.check_output(split(cmd))
        except subprocess.CalledProcessError as expect:
            print("Error: ", expect.returncode, expect.output)

    def login(self, user, password, email, registry=None):
        '''
        Docker login exposed as a method.

        :param user:  Username in the registry
        :param password: - Password for the registry
        :param email: - Email address on account (dockerhub)
        '''
        cmd = ['docker', 'login', '-u', user, '-p', password, '-e', email]
        if registry:
            cmd.append(registry)
        subprocess.check_call(cmd)

    def logs(self, container_id, raise_on_failure=False):
        '''
        Docker logs exposed as a method.

        :param container_id: - UUID for the container to fetch logs
        '''
        cmd = ['docker', 'logs', container_id]
        output = subprocess.check_output(cmd)

        return output.decode('ascii', 'ignore')

    def ps(self):
        '''
        return a string of docker status output
        '''
        cmd = ['docker', 'ps']
        return subprocess.check_output(cmd)

    def pull(self, image):
        '''
        Pull an image from the docker hub
        '''
        cmd = ['docker', 'pull', image]
        return subprocess.check_output(cmd)
