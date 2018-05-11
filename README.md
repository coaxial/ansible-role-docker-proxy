Docker Proxy
=========

Reverse proxy in a Docker container to streamline services and easily setup HTTPS.

Requirements
------------

- Docker

Role Variables
--------------

<table>
<tr>
  <th>Name</th>
  <th>Default value</th>
  <th>Possible values</th>
  <th>Purpose</th>
</tr>
<tr>
  <td>`dp__upstream_ports`</td>
  <td>none, must be set</td>
  <td>
    <pre lang="yaml">
dp__upstream_ports:
  - port: 1234
  - port: 4567
  - port: 8900
  ...
    </pre>
  </td>
  <td>
    Ports for the services to put behind the proxy. These ports must be bound to localhost (at least)
  </td>
</tr>
<tr>
  <td>`dp__https_enable`</td>
  <td>`true`</td>
  <td>`true` or `false`</td>
  <td>Enable or disable HTTPS</td>
</tr>
</table>

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in
regards to parameters that may need to be set for other roles, or variables that
are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: ansible-role-docker-proxy, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a
website (HTML is not allowed).
