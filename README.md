Docker Proxy
=========

Reverse proxy in a Docker container to streamline services and easily setup HTTPS.

Requirements
------------

- Docker

Role Variables
--------------

### `dp__upstream`
#### Default value
none, must be set
#### Possible values/example
```yaml
dp__upstream:
  - port: 1234  # port the upstream webserver exposes
    svc_name: nginx  # name for the webserver service in the original compose file
    project_src: /opt/docker-app1/  # location for the original compose file on the host
    vhost: app1.example.org  # subdomain you want the service accessible from
    default_net: true  # attach svc_name to the default docker-compose network as well (cf. https://docs.docker.com/compose/networking/#configure-the-default-network), defaults to false
    doco: docker-compose.prod.yml  # docker-compose.yml filename, defaults to docker-compose.yml (optional)
  - port: 4567
    svc_name: webserver
    project_src: /opt/docker-app2/
  - port: 8900
    svc_name: app3
    project_src: /opt/docker-app3/
  ...
```
#### Purpose
Describes the services to put behind the proxy, and how to access them.

### `dp__le_enable`
#### Default value
`true`
#### Possible values
`true` or `false`
#### Purpose
Enable or disable HTTPS and let's encrypt certificates.

### `dp__ipv6_enable`
#### Default value
`true`
#### Possible values
`true` or `false`
#### Purpose
Enable or disable IPv6.

### `dp__le_enable`
#### Default value
`true`
#### Possible values
`true` or `false`
#### Purpose
Enable or disable lets encrypt certificate auto-renewal.

### `dp__le_email`
#### Default value
none, must be set if `dp__le_enable` is `true`
#### Possible values
any valid email address
#### Purpose
Used by Let's Encrypt to warn of expiring certificates should the auto-renewal fail, and for account recovery.

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
