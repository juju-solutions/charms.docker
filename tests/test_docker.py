from charms.docker import Docker
from mock import patch
import pytest
from subprocess import CalledProcessError


class TestDocker:

    @pytest.fixture
    def docker(self):
        return Docker()

    # There's a pattern to run an isolated docker daemon to run supporting
    # infrastructure of the primary docker daemon. This bootstrap daemon
    # runs host only on a socket
    @pytest.fixture
    def bootstrap(self):
        return Docker(socket="unix:///var/run/docker-bootstrap.sock")

    def test_docker_init_defaults(self, docker):
        docker.socket = "unix:///var/run/docker.sock"

    def test_docker_init_socket(self):
        docker = Docker(socket="tcp://127.0.0.1:2357")
        assert docker.socket == "tcp://127.0.0.1:2357"

    def test_docker_init_workspace(self):
        devel = Docker(workspace="files/tmp")
        assert "{}".format(devel.workspace) == "files/tmp"

    def test_kill(self, docker):
        with patch('charms.docker.Docker._run') as rp:
            docker.kill('12345')
            rp.assert_called_with('kill 12345')

    @patch('charms.docker.Docker.wait')
    @patch('charms.docker.Docker.rm')
    @patch('charms.docker.Docker.kill')
    def test_pedantic_kill(self, kmock, rmock, wmock, docker):
        docker.pedantic_kill('12345')
        kmock.assert_called_with('12345')
        wmock.assert_called_with('12345')
        rmock.assert_called_with('12345', True, True)

    def test_logs(self, docker):
        with patch('subprocess.check_output') as spmock:
            docker.logs('6f137adb5d27')
            spmock.assert_called_with(['docker',  '-H',
                                       'unix:///var/run/docker.sock',
                                       'logs', '6f137adb5d27'])

    def test_login(self, docker):
        with patch('subprocess.check_call') as spmock:
            docker.login('cloudguru', 'XXX', 'obrien@ds9.org')
            spmock.assert_called_with(['docker',  '-H',
                                       'unix:///var/run/docker.sock',
                                       'login', '-u', 'cloudguru',
                                       '-p', 'XXX', '-e', 'obrien@ds9.org'])

    def test_login_registry(self, docker):
        with patch('subprocess.check_call') as spmock:
            docker.login('cloudguru', 'XXX', 'obrien@ds9.org',
                         registry='test:1234')
            spmock.assert_called_with(['docker', '-H',
                                       'unix:///var/run/docker.sock', 'login',
                                       '-u', 'cloudguru',
                                       '-p', 'XXX', '-e', 'obrien@ds9.org',
                                       'test:1234'])

    def test_ps(self, docker):
        with patch('subprocess.check_output') as rp:
            docker.ps()
            rp.assert_called_with(['docker', '-H',
                                   'unix:///var/run/docker.sock',
                                   'ps'])

    def test_pull(self, docker):
        with patch('subprocess.check_output') as spmock:
            docker.pull('tester/testing')
            spmock.assert_called_with(['docker',  '-H',
                                       'unix:///var/run/docker.sock',
                                       'pull', 'tester/testing'])

    def test_running(self, bootstrap, docker):
        with patch('subprocess.check_call') as call_mock:
            bootstrap.running()
            call_mock.assert_called_with(['docker', '-H',
                                          'unix:///var/run/docker-bootstrap.sock',  # noqa
                                          'info'])
            docker.running()
            call_mock.assert_called_with(['docker', '-H',
                                          'unix:///var/run/docker.sock',
                                          'info'])


    def test_run(self, docker):
        with patch('subprocess.check_output') as spmock:
            docker.run(image='nginx')
            spmock.assert_called_with(['docker', '-H',
                                       'unix:///var/run/docker.sock',
                                       'run', 'nginx'])
            docker.run('nginx', ['-d --name=nginx'])
            spmock.assert_called_with(['docker',  '-H',
                                       'unix:///var/run/docker.sock',
                                       'run', '-d', '--name=nginx',
                                       'nginx'])

    def test_wait(self, docker):
        with patch('charms.docker.Docker._run') as rp:
            docker.wait('12345')
            rp.assert_called_with('wait 12345')

    def test_rm(self, docker):
        with patch('charms.docker.Docker._run') as rp:
            docker.rm('12345', True, True)
            rp.assert_called_with('rm -f -v 12345')

    def test_load(self, docker):
        with patch('charms.docker.Docker._run') as rp:
            docker.load('/path/to/image')
            rp.assert_called_with('load -i /path/to/image')
