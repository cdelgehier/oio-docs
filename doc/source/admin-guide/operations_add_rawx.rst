==================
Add a rawx service
==================

.. contents::
   :local:

Description
-----------
In this documentation, you will find the different steps to add a new rawx service on your cluster.

In this example, we will add a new rawx service (rawx-2) in the namespace OPENIO on an existing server:

Furthermore, to secure your new rawx service, you will have two options:
  - assign an existing rdir to your new rawx
  - install a new rdir service (rdir-2) and assign it to your new rawx
Both options will be detailled here after.

Prerequisites
-------------

You must have the IPs and PORTs that will be used for your new services.
In this example:

- the new rawx will listen on ``10.0.0.36:6211``
- the new rdir will listen on ``10.0.0.39:6302``

Configuration
-------------

Configure a new rawx
++++++++++++++++++++

Create an new directory ``/rawx-2`` in ``/var/lib/oio/sds/OPENIO/``

Give the rights on this directory to the openio user:

.. code-block:: text

    $ chown openio.openio rawx-2/


Create an new directory ``/rawx-2`` in ``/etc/oio/sds/OPENIO/``

Give the rights on this directory to the openio user:

.. code-block:: text

    $ chown openio.openio rawx-2/

Create a new configuration file (``rawx-2-httpd.conf``) in your new created directory ``/etc/oio/sds/OPENIO/rawx-2``:

.. code-block:: shell
   :caption: /etc/oio/sds/OPENIO/rawx-2/rawx-2-httpd.conf

   LoadModule mpm_worker_module   /usr/lib64/httpd/modules/mod_mpm_worker.so
   LoadModule authz_core_module   /usr/lib64/httpd/modules/mod_authz_core.so
   LoadModule dav_module          /usr/lib64/httpd/modules/mod_dav.so
   LoadModule mime_module         /usr/lib64/httpd/modules/mod_mime.so
   LoadModule dav_rawx_module     /usr/lib64/httpd/modules/mod_dav_rawx.so
   LoadModule setenvif_module     /usr/lib64/httpd/modules/mod_setenvif.so
   LoadModule alias_module        /usr/lib64/httpd/modules/mod_alias.so
   LoadModule env_module          /usr/lib64/httpd/modules/mod_env.so
   LoadModule unixd_module        /usr/lib64/httpd/modules/mod_unixd.so
   LoadModule log_config_module   /usr/lib64/httpd/modules/mod_log_config.so
   LoadModule logio_module        /usr/lib64/httpd/modules/mod_logio.so

   Alias / /x/

   Listen          10.0.0.36:6211
   PidFile         /run/oio/sds/OPENIO-rawx-2-httpd.pid
   ServerRoot      /var/lib/oio/sds/OPENIO/coredump
   ServerName      localhost
   ServerSignature Off
   ServerTokens    Prod
   DocumentRoot    /var/lib/oio/sds/OPENIO/rawx-2
   TypesConfig     /etc/mime.types

   User  openio
   Group openio

   SetEnv INFO_SERVICES OIO,OPENIO,rawx,2
   SetEnv LOG_TYPE access
   SetEnv LEVEL INF
   SetEnv HOSTNAME node-1.novalocal

   SetEnvIf Remote_Addr "^" log-cid-out=1
   SetEnvIf Remote_Addr "^" log-cid-in=0
   SetEnvIf Request_Method "PUT" log-cid-in=1
   SetEnvIf Request_Method "PUT" !log-cid-out
   SetEnvIf log-cid-in 0 !log-cid-in

   LogFormat "%{%b %d %T}t %{HOSTNAME}e %{INFO_SERVICES}e %{pid}P %{tid}P %{LOG_TYPE}e %{LEVEL}e %{Host}i %a:%{remote}p %m %>s %D %I %{x-oio-chunk-meta-container-id}i %{x-oio-req-id}i %U" log/cid-in
   LogFormat "%{%b %d %T}t %{HOSTNAME}e %{INFO_SERVICES}e %{pid}P %{tid}P %{LOG_TYPE}e %{LEVEL}e %{Host}i %a:%{remote}p %m %>s %D %O %{x-oio-chunk-meta-container-id}o %{x-oio-req-id}i %U" log/cid-out

   ErrorLog /var/log/oio/sds/OPENIO/rawx-2/rawx-2-httpd-errors.log
   SetEnvIf Request_URI "/(stat|info)$" nolog=1

   SetEnvIf nolog 1 !log-cid-out
   SetEnvIf nolog 1 !log-cid-in

   CustomLog /var/log/oio/sds/OPENIO/rawx-2/rawx-2-httpd-access.log log/cid-out env=log-cid-out
   CustomLog /var/log/oio/sds/OPENIO/rawx-2/rawx-2-httpd-access.log log/cid-in  env=log-cid-in

   <IfModule worker.c>
   MaxRequestsPerChild 0
   MaxSpareThreads 256
   MinSpareThreads 32
   ServerLimit 16
   StartServers 1
   ThreadsPerChild 256
   </IfModule>


   DavDepthInfinity Off

   grid_docroot    /var/lib/oio/sds/OPENIO/rawx-2
   # How many hexdigits must be used to name the indirection directories
   grid_hash_width 3
   # How many levels of directories are used to store chunks
   grid_hash_depth 1
   # At the end of an upload, perform a fsync() on the chunk file itself
   grid_fsync      enabled
   # At the end of an upload, perform a fsync() on the directory holding the chunk
   grid_fsync_dir  enabled
   # Preallocate space for the chunk file (enabled by default)
   #grid_fallocate enabled
   # Enable compression ('zlib' or 'lzo' or 'off')
   grid_compression off
   grid_namespace  OPENIO
   grid_dir_run    /run/oio/sds

   <Directory />
   DAV rawx
   AllowOverride None
   Require all granted
   Options -SymLinksIfOwnerMatch -FollowSymLinks -Includes -Indexes
   </Directory>

   <VirtualHost 10.0.0.36:6211>
   # DO NOT REMOVE (even if empty) !
   </VirtualHost>


The following configuration must be adapted to your new service:

- Listen
- PidFile        
- DocumentRoot 
- SetEnv
- ErrorLog
- CustomLog
- grid_docroot
- VirtualHost

Create a new configuration file (``OPENIO-rawx-2``) in the ``/etc/gridinit.d/`` directory:

.. code-block:: shell
   :caption: /etc/gridinit.d/OPENIO-rawx-2

   [Service.OPENIO-rawx-2]
   command=/usr/sbin/httpd -D FOREGROUND -f /etc/oio/sds/OPENIO/rawx-2/rawx-2-httpd.conf
   enabled=true
   start_at_boot=yes
   on_die=respawn
   group=OPENIO,rawx,rawx-2
   uid=openio
   gid=openio
   env.PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin

Create a new configuration file (``rawx-2.yml``) in the ``/etc/oio/sds/OPENIO/watch/`` directory:

.. code-block:: shell
   :caption: /etc/oio/sds/OPENIO/watch/rawx-2.yml

   host: 10.0.0.36
   port: 6211
   type: rawx
   location: node-1
   checks:
   - {type: http, uri: /info}
   stats:
   - {type: volume, path: /var/lib/oio/sds/OPENIO/rawx-2}
   - {type: rawx, path: /stat}
   - {type: system}

The following configuration must be adapted to your new service:

- host
- port        
- type: volume, path

Then, to make your new rawx service available, you have to reload the configuration and start the service:

.. code-block:: text

    $ gridinit_cmd reload
    $ gridinit_cmd start OPENIO-rawx-2

And to restart the conscience agent:

.. code-block:: text

    $ gridinit_cmd restart @conscienceagent



Configure a new rdir (optionnal)
++++++++++++++++++++++++++++++++

In order to secure the new rawx, you can install a new rdir service on another server.

Create an new directory ``/rdir-2`` in ``/var/lib/oio/sds/OPENIO/``

Give the rights on this directory to the openio user:

.. code-block:: text

    $ chown openio.openio rdir-2/


Create an new directory ``/rdir-2`` in ``/etc/oio/sds/OPENIO/``

Give the rights on this directory to the openio user:

.. code-block:: text

    $ chown openio.openio rdir-2/

Create a new configuration file (``rdir-2.conf``) in your new created directory ``/etc/oio/sds/OPENIO/rdir-2``:

.. code-block:: shell
   :caption: /etc/oio/sds/OPENIO/rdir-2/rdir-2.conf

   [rdir-server]
   bind_addr = 10.0.0.39
   bind_port = 6302
   namespace = OPENIO
   # Currently, only 1 worker is allowed to avoid concurrent access to leveldb database
   workers = 1
   worker_class = sync
   threads = 1
   db_path= /var/lib/oio/sds/OPENIO/rdir-2
   log_facility = LOG_LOCAL0
   log_level = info
   log_address = /dev/log
   syslog_prefix = OIO,OPENIO,rdir,2

Create a new configuration file (``OPENIO-rdir-2``) in the ``/etc/gridinit.d/`` directory:

.. code-block:: shell
   :caption: /etc/gridinit.d/OPENIO-rdir-2

   enabled=true
   start_at_boot=yes
   on_die=respawn
   group=OPENIO,rdir,rdir-2
   uid=openio
   gid=openio
   env.PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin

Create a new configuration file (``rdir-2.yml``) in the ``/etc/oio/sds/OPENIO/watch/`` directory:

.. code-block:: shell
    :caption: /etc/oio/sds/OPENIO/watch/rdir-2.yml

    host: 10.0.0.39
    port: 6302
    type: rdir
    location: yb-2
    checks:
      - {type: tcp}
    stats:
      - {type: volume, path: /var/lib/oio/sds/OPENIO/rdir-2}
      - {type: http, path: /status, parser: json}
      - {type: system}

Then, to make your new rdir service available, you have to reload the configuration and start the service:

.. code-block:: text

    $ gridinit_cmd reload
    $ gridinit_cmd start OPENIO-rdir-2

And to restart the conscience agent:

.. code-block:: text

    $ gridinit_cmd restart @conscienceagent

Then, you will have to unlock your new service:

.. code-block:: text

    $ openio cluster unlock rdir 10.0.0.39:6302


Rdir assignation
++++++++++++++++

In order to secure the new rawx, you must asign your new rawx to a rdir service.

In the example below, you can see that the new rawx (10.0.0.36:6211) has no rdir assignation, and your new rdir (10.0.0.39:6302) does not manage any rawx:

.. code-block:: text

    $ openio volume assignation --aggregated
    +----------------+-----------------+----------------+
    | Rdir           | Number of bases | Bases          |
    +----------------+-----------------+----------------+
    | 10.0.0.36:6301 |               1 | 10.0.0.37:6201 |
    | 10.0.0.37:6301 |               1 | 10.0.0.38:6201 |
    | 10.0.0.39:6302 |               0 |                |
    | 10.0.0.38:6301 |               1 | 10.0.0.36:6201 |
    | n/a            |               1 | 10.0.0.36:6211 |
    +----------------+-----------------+----------------+

Whether you have installed a new rdir or not, you will have to launch the following command to create the assignation:

.. code-block:: text

    $ openio volume admin bootstrap
    +----------------+----------------+---------------+---------------+
    | Rdir           | Rawx           | Rdir location | Rawx location |
    +----------------+----------------+---------------+---------------+
    | 10.0.0.36:6301 | 10.0.0.37:6201 | yb-1          | yb-2          |
    | 10.0.0.37:6301 | 10.0.0.38:6201 | yb-2          | yb-3          |
    | 10.0.0.37:6301 | 10.0.0.36:6211 | yb-2          | yb-1          |
    | 10.0.0.38:6301 | 10.0.0.36:6201 | yb-3          | yb-1          |
    +----------------+----------------+---------------+---------------+


Finalize the installation
+++++++++++++++++++++++++

Finally, you will have to unlock your new service:

.. code-block:: text

    $ openio cluster unlock rawx 10.0.0.36:6211


You can check that your new service is available using the ``openio cluster list`` command:

.. code-block:: text

    $ openio cluster list

    +---------+----------------+------------+---------------------------------+------------+-------+------+-------+
    | Type    | Addr           | Service Id | Volume                          | Location   | Slots | Up   | Score |
    +---------+----------------+------------+---------------------------------+------------+-------+------+-------+
    | account | 10.0.0.38:6009 | n/a        | n/a                             | node-3     | n/a   | True |    96 |
    | account | 10.0.0.36:6009 | n/a        | n/a                             | node-1     | n/a   | True |    95 |
    | account | 10.0.0.37:6009 | n/a        | n/a                             | node-2     | n/a   | True |    98 |
    | meta0   | 10.0.0.38:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | node-3     | n/a   | True |    98 |
    | meta0   | 10.0.0.36:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | node-1     | n/a   | True |    97 |
    | meta0   | 10.0.0.37:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | node-2     | n/a   | True |    98 |
    | meta1   | 10.0.0.38:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | node-3     | n/a   | True |    92 |
    | meta1   | 10.0.0.36:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | node-1     | n/a   | True |    90 |
    | meta1   | 10.0.0.37:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | node-2     | n/a   | True |    92 |
    | meta2   | 10.0.0.38:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | node-3     | n/a   | True |    91 |
    | meta2   | 10.0.0.36:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | node-1     | n/a   | True |    90 |
    | meta2   | 10.0.0.37:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | node-2     | n/a   | True |    92 |
    | rawx    | 10.0.0.36:6211 | n/a        | /var/lib/oio/sds/OPENIO/rawx-2  | node-1     | n/a   | True |    90 |
    | rawx    | 10.0.0.38:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | node-3     | n/a   | True |    92 |
    | rawx    | 10.0.0.36:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | node-1     | n/a   | True |    90 |
    | rawx    | 10.0.0.37:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | node-2     | n/a   | True |    91 |
    | rdir    | 10.0.0.38:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | node-3     | n/a   | True |    97 |
    | rdir    | 10.0.0.36:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | node-1     | n/a   | True |    95 |
    | rdir    | 10.0.0.37:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | node-2     | n/a   | True |    97 |
    +---------+----------------+------------+---------------------------------+------------+-------+------+-------+
