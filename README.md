Docker Proxy
=========

Reverse proxy in a Docker container to streamline services and easily setup HTTPS.

Requirements
------------

- Docker

Role Variables
--------------

### `dp__upstream_ports`
#### Default value
none, must be set
#### Possible values
```yaml
dp__upstream_ports:
  - port: 1234
  - port: 4567
  - port: 8900
  ...
```
#### Purpose
Ports for the services to put behind the proxy. These ports must be bound to localhost (at least)

### `dp__https_enable`
#### Default value
`true`
#### Possible values
`true` or `false`
#### Purpose
Enable or disable HTTPS

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
