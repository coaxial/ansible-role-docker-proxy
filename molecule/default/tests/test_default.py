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
    r = host.iptables.rules()

    assert "-A DOCKER-USER -i eth0 -p tcp -m tcp --dport 5000 -j DROP" in r
