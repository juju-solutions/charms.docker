from charms.docker import Compose
from mock import patch
import os
import pytest


class TestCompose:

    # This has limited usefulness, it fails when used with the @patch
    # decorator. simply pass in compose to any object to gain the
    # test fixture
    @pytest.fixture
    def compose(self):
        return Compose('files/test', strict=False)

    def test_init_strict(self):
        with patch('charms.docker.compose.Workspace.validate') as f:
            Compose('test', strict=True)
            # Is this the beast? is mock() doing the right thing here?
            f.assert_called_with()

    def test_init_workspace(self, compose):
        assert "{}".format(compose.workspace) == "files/test"

    def test_build(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.build()
            s.assert_called_with('docker-compose build --force-rm',
                                 compose.workspace, None)
            compose.build('foobar')
            expect = 'docker-compose build --force-rm foobar'
            s.assert_called_with(expect, compose.workspace, None)

            compose.build('foobar', no_cache=True, pull=True)
            expect = 'docker-compose build --force-rm --no-cache --pull foobar'
            s.assert_called_with(expect, compose.workspace, None)

            compose.build('foobar', force_rm=False)
            expect = 'docker-compose build foobar'
            s.assert_called_with(expect, compose.workspace, None)

            compose.build(no_cache=True)
            expect = 'docker-compose build --force-rm --no-cache'

    def test_kill_service(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.kill('nginx')
            expect = 'docker-compose kill nginx'
            s.assert_called_with(expect, compose.workspace, None)

    def test_kill_service_default(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.kill()
            expect = 'docker-compose kill'
            s.assert_called_with(expect, compose.workspace, None)

    def test_pull_service(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.pull('nginx')
            s.assert_called_with('docker-compose pull nginx',
                                 compose.workspace, None)

    def test_pull_service_default(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.pull()
            s.assert_called_with('docker-compose pull', compose.workspace,
                                 None)

    def test_restart(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.restart('nginx')
            s.assert_called_with('docker-compose restart nginx',
                                 compose.workspace, None)

    def test_restart_default(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.restart()
            s.assert_called_with('docker-compose restart', compose.workspace,
                                 None)

    def test_up_service(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.up('nginx')
            expect = 'docker-compose up -d nginx'
            s.assert_called_with(expect, compose.workspace, None)

    def test_up_default_formation(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.up()
            expect = 'docker-compose up -d'
            s.assert_called_with(expect, compose.workspace, None)

    def test_start_service(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.start('nginx')
            expect = 'docker-compose start nginx'
            s.assert_called_with(expect, compose.workspace, None)

    def test_rm_service_default(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.rm()
            expect = 'docker-compose rm -f'
            s.assert_called_with(expect, compose.workspace, None)

    def test_rm_service(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.rm('nginx')
            expect = 'docker-compose rm -f nginx'
            s.assert_called_with(expect, compose.workspace, None)

    def test_scale(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.scale('nginx', 3)
            expect = 'docker-compose scale nginx=3'
            s.assert_called_with(expect, compose.workspace, None)

    def test_stop_service(self, compose):
        with patch('charms.docker.compose.run') as s:
            compose.stop('nginx')
            expect = 'docker-compose stop -t 10 nginx'
            s.assert_called_with(expect, compose.workspace, None)

    @patch('charms.docker.runner.chdir')
    @patch('charms.docker.runner.check_output')
    def test_run(self, ccmock, chmock):
        compose = Compose('files/workspace', strict=False)
        compose.up('nginx')
        chmock.assert_called_with('files/workspace')
        ccmock.assert_called_with(['docker-compose', 'up', '-d', 'nginx'])

    @patch('charms.docker.runner.chdir')
    @patch('charms.docker.runner.check_output')
    def test_socket_run_has_host_output(self, ccmock, chmock):
        compose = Compose('files/workspace', strict=False, socket='test')
        compose.up()
        chmock.assert_called_with('files/workspace')
        ccmock.assert_called_with(['docker-compose', 'up', '-d'])
        assert(os.getenv('DOCKER_HOST') == 'test')

    # This test is a little ugly but is a byproduct of testing the callstack.
    @patch('os.getcwd')
    def test_context_manager(self, cwdmock):
        cwdmock.return_value = '/tmp'
        with patch('os.chdir') as chmock:
            compose = Compose('files/workspace', strict=False)
            with patch('charms.docker.runner.check_output'):
                compose.up('nginx')
                # We can only test the return called with in this manner.
                # So check that we at least reset context
                chmock.assert_called_with('/tmp')
                # TODO: test that we've actually tried to change dir context
