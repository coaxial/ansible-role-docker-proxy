Docker Proxy
=========

Reverse proxy in a Docker container to streamline services and easily setup HTTPS.

[![Build Status](https://travis-ci.org/coaxial/ansible-role-docker-proxy.svg?branch=master)](https://travis-ci.org/coaxial/ansible-role-docker-proxy)

Requirements
------------

- Docker

Role Variables
--------------

- ### `dp__upstream`

  Default value | Possible values | Purpose
  ---|---|---
  none, must be set | cf. example below | Describes the services to put behind the proxy, and how to access them.

  Example:
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

- ### `dp__ipv6_enable`

  Default value | Possible values | Purpose
  ---|---|---
  `true`|`true` or `false`|Enable or disable IPv6.

- ### `dp__le_enable`

  Default value | Possible values | Purpose
  ---|---|---
  `true` | `true` or `false` | Enable or disable lets encrypt certificate auto-renewal.

- ### `dp__le_test`

  Default value | Possible values | Purpose
  ---|---|---
  `false`| `true` or `false`| Use lets encrypt's testing servers instead of the lives one to avoid rate limiting (5 certs/week, it happens very quickly)

- ### `dp__le_email`

  Default value | Possible values | Purpose
  ---|---|---
  none, must be set if `dp__le_enable` is `true`| any valid email address| Used by Let's Encrypt to warn of expiring certificates should the auto-renewal fail, and for account recovery.

- ### `dp__le_timeout`

  Default value | Possible values | Purpose | Notes
  ---|---|---|---
  `300` | Any integer | The lets encrypt container needs to generate its DH params before it listens to upstream servers restarts and starts getting certs for them. This is the amount of time it takes to generate the DH params and for while the playbook's execution stops after starting the lets encrypt container. | It's possible this value is too high, so it can be overridden. The value is the number of seconds to wait for the lets encrypt container to start. For example, 120 seconds is usually enough on a 5$ DigitalOcean droplet.

Dependencies
------------

n/a

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:

    - hosts: servers
      become: true
      vars:
        dp__le_timeout: 120
        dp__le_email: test@example.org
        dp__upstream:
          - port: 5000
            svc_name: webapp
            project_src: /opt/webapp
            vhost: test.example.org
      roles:
        - role: ansible-role-docker-proxy

License
-------

BSD

Author Information
------------------

coaxial <https://64b.it>
