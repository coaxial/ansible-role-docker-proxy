import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_firewall(host):
    r = host.iptables.rules('filter', 'DOCKER-USER')

    assert "-A DOCKER-USER -i eth0 -p tcp -m tcp --dport 5000 -j DROP" in r


def test_compose_extends(host):
    dc = host.file('/opt/webapp/docker-compose.proxy.yml')

    assert dc.exists
    assert dc.user == 'root'
    assert dc.group == 'root'
    assert dc.mode == 0o400
    assert dc.contains('webapp:')
    assert dc.contains('VIRTUAL_HOST=test.example.org')
    assert dc.contains('VIRTUAL_PORT=5000')
    assert dc.contains('LETSENCRYPT_HOST=test.example.org')
    assert dc.contains('LETSENCRYPT_EMAIL=test@example.org')
    assert dc.contains('LETSENCRYPT_TEST=true')
    assert dc.contains('upstreams:')
    assert dc.contains('- upstreams')


def test_nginx_proxy(host):
    d = host.file('/opt/nginx-proxy')
    t = host.file('/opt/nginx-proxy/nginx.tmpl')

    for item in [d, t]:
        assert item.exists
        assert item.user == 'root'
        assert item.group == 'root'

    assert d.mode == 0o755
    assert t.mode == 0o400


def test_proxy_bypass(host):
    host.run('sudo apt install curl -yq')
    FAILED_TO_CONNECT_TO_HOST_EXIT_CODE = 7

    assert host.run_expect(
        [FAILED_TO_CONNECT_TO_HOST_EXIT_CODE],
        'curl -sfL http://localhost'
    )


def test_proxy(host):
    webpage = host.check_output('http://localhost:5000')

    assert "Hello world" in webpage
