Docker Proxy
=========

Reverse proxy in a Docker container to streamline services and easily setup HTTPS. Will respect exisiting docker-compose.yml overrides.

[![Build Status](https://travis-ci.org/coaxial/ansible-role-docker-proxy.svg?branch=master)](https://travis-ci.org/coaxial/ansible-role-docker-proxy)

Requirements
------------

- Docker
- docker-compose

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
      doco: docker-compose.prod.yml  # docker-compose.yml filename, defaults to docker-compose.yml (optional)
    - port: 4567
      svc_name: webserver
      project_src: /opt/docker-app2/
      vhost: www.example.org
      is_container: true
    - port: 8900
      svc_name: app3
      project_src: /opt/docker-app3/
      vhost: app3.example.org
      is_container: true
    # if the app to proxy isn't in a container, specify it this way:
    - port: 9100  # port the webserver runs on
      svc_name: prom_node_exporter  # a canonical name for the service
      vhost: metrics.example.org
      is_container: false
      bauth_enable: true
      bauth_user: username
      bauth_passwd: s3cur3
    ...
  ```

  This variable describes the services to reverse-proxy. They can either be running within docker containers (`is_container` set to `true`) or directly on the host (must be accessible via localhost:port, `is_container` set to `false`.)

  For non-docker (a.k.a. "metal") services, a custom server configuration file can be used. This is optional, it will use `templates/default.conf.j2` by default. To override, create a file a `templates/{{ upstream.svc_name }}.conf.j2` and  the role will pick it up for that service. Note that the role expects the custom nginx server to listen on port 80, and you can use `_dp__docker_gw_ip` for the docker host's gateway IP address to communicate with a service running on the docker host. See the tests at `molecule/{custom,bauth}` for more context.

  To protect a "metal" service with basic auth, set `bauth_enable` to `true`, define the username as `bauth_user` and the password as `bauth_passwd`. This will generate a `<svc_name>.htpasswd` at `dp__nginx_config_dir` (`/opt/non-docker-nginx` by default) that will be mounted at `/etc/nginx/.htpasswd` within the nginx proxy container. You can use the `.htpasswd` file in your custom nginx configuration if needed.

  If you would like to protect a containerized service with basic auth, I suggest creating a synthetic "metal" service with a custom nginx server config file that will proxy requests to the containerized service. You will be able to enable basic auth with a custom server config, and `proxy_pass` to localhost:container_port. For example, if I want to run `mywebapp` in a container on port 5000, I will create an upstream as follows:
  ```yaml
  - port: 5000
    svc_name: mywebapp
    vhost: mywebapp.example.com
    is_container: false
    bauth_enable: true
    bauth_user: user
    bath_passwd: passwd
  ```
  and create `templates/mywebapp.conf.j2` to go with it:
  ```nginx
  server {
    listen 80; # always port 80, don't change it

    location / {
      auth_basic: "Restricted";
      auth_basic_user_file: /etc/nginx/.htpasswd;
      # _dp__docker_gw_ip is defined by the role, it's the docker host's IP
      # So anything accessible via localhost on the docker host will be accessible
      # via this IP from a container
      proxy_pass http://{{ _dp__docker_gw_ip }}:{{ upstream.port }};
    }
  }
  ```

  For examples on how to use a custom server config file and basic auth, see `molecule/{custom,bauth}/playbook.yml`.

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

- ### `dp__nginx_config_dir`

  Default value | Possible values | Purpose | Notes
  ---|---|---|---
  `/opt/non-docker-nginx` | any valid path | Where to keep the nginx proxy config files for non-docker upstream services

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

Questions or issues
-------------------

Open an issue and I'll do my best to help out/clarify. PRs welcome.

License
-------

MIT

Author Information
------------------

coaxial <https://64b.it>
