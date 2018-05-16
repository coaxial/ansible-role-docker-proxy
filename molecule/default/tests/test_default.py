import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_firewall(host):
    r = host.iptables.rules('filter', 'DOCKER-USER')

    assert "-A DOCKER-USER -i eth0 -p tcp -m tcp --dport 5000 -j DROP" in r


def test_compose_extends(host):
    dc = host.file('/opt/webapp/docker-compose.proxy.yml')

    assert dc.exists
    assert dc.user == 'root'
    assert dc.group == 'root'
    assert dc.contains('webapp:')
    assert dc.contains('VIRTUAL_HOST=test.example.org')
    assert dc.contains('VIRTUAL_PORT=5000')
    assert dc.contains('LETSENCRYPT_HOST=test.example.org')
    assert dc.contains('LETSENCRYPT_EMAIL=test@example.org')
    assert not dc.contains('LETSENCRYPT_TEST=true')
    assert dc.contains('upstreams:')
    assert dc.contains('- upstreams')
