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
    host.run('sudo apt install daemon curl netcat-openbsd -yq')
    # start non-containerized web server within the Ansible configured machine
    # host.run(
    #     'nohup sh -c \'while true; do printf "HTTP/1.1 200 OK\r\n'
    #     'Content-length: 14\r\n\r\nHello world!\r\n" | nc -q 1 -l -p 1500; '
    #     'done\' &; exit 0'
    # )
    # host.run(
    #     '(printf "HTTP/1.1 200 OK\r\n'
    #     'Content-length: 13\r\n\r\nHello world!\r\n" | nc -q 1 -l -p 1500 &)'
    #     ' && curl -vL http://localhost:1500'
    # )
    host.run(
        'daemon --name=nc '
        'sh -c \'while true; do printf "HTTP/1.1 200 OK\r\n'
        'Content-length: 14\r\n\r\nHello world!\r\n" | nc -q 1 -l -p 1500; '
        'done\''
        ' && curl -vL http://localhost:1500'
    )
    webpage = host.check_output('curl -vL http://localhost')
    # webpage = host.check_output('curl -sfL http://localhost')

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
