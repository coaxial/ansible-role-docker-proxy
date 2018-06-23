import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_firewall(host):
    r = host.iptables.rules('filter', 'DOCKER-USER')

    assert "-A DOCKER-USER -i eth0 -p tcp -m tcp --dport 1500 -j DROP" in r


def test_compose_extends(host):
    dc = host.file('/opt/webapp/docker-compose.proxy.yml')

    assert not dc.exists


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
    host.run('sudo apt install curl netcat-openbsd -yq')
    # Make test.example.org resolve so that it can be curled and nginx-proxy
    # knows which container to forward it to based on the headers
    host.run('echo "127.0.0.1 test.example.org" >> /etc/hosts')
    webpage = host.check_output(
        # This is a minimal webserver that will answer with 200 OK
        # and Hello world!
        'sh -c \'(while true; do printf "HTTP/1.1 200 OK\r\n'
        'Content-length: 13\r\nContent-type: text/plain\r\n\r\n'
        'Hello world!\r\n" | nc -q 1 -l -p 1500;'
        ' done) &\''
        # Query the minimal webserver through nginx-proxy
        ' && curl -sfL test.example.org'
    )

    assert "Hello world!" in webpage


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
