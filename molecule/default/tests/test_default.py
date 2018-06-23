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


def test_proxy(host):
    host.run('sudo apt install curl -yq')
    # Make test.example.org resolve
    host.run('echo "127.0.0.1 test.example.org" >> /etc/hosts')
    # webpage = host.check_output('curl -sfL http://localhost')
    webpage = host.check_output('curl -vL http://test.example.org')

    assert "Thank you for using nginx." in webpage


def test_ssl_certs_volume(host):
    volumes = host.check_output('docker volume list')

    assert "ssl_certs" in volumes


def test_nginx_template(host):
    f = host.file('/opt/nginx-proxy/nginx.tmpl')

    assert f.exists


def test_containers_start(host):
    services = ['nginx-proxy', 'nginx-gen', 'nginx-le']

    for service in services:
        container_full_name = host.check_output(
            "docker ps -f 'name={0}' ".format(service) +
            "{% raw %}--format='{{.Names}}'{% endraw %}"
        )

    assert service in container_full_name
