===================
Add a meta2 service
===================


Description
-----------
In this documentation, you will find the different steps to add a new meta2 service on your cluster.

In this example, we add a new rawx service (meta2-2) in the namespace OPENIO on an existing server.

Prerequisites
-------------

You must have the IP and PORT of your new meta2 service. In this example, the new meta2 will listen on 10.0.0.36:6122

Configuration
-------------

Create an new directory ``/meta2-2`` in ``/var/lib/oio/sds/OPENIO/``

Give the rights on this directory to the openio user:

.. code-block:: text

    $ chown openio.openio meta2-2/

Create a new configuration file (``OPENIO-meta2-2``) in the ``/etc/gridinit.d/`` directory:

.. code-block:: shell
   :caption: /etc/gridinit.d/OPENIO-meta2-2

   [Service.OPENIO-meta2-2]
   command=/usr/bin/oio-meta2-server   -p /run/oio/sds/OPENIO-meta2-2.pid -s OIO,OPENIO,meta2,2 -O Endpoint=10.0.0.36:6122 OPENIO /var/lib/oio/sds/OPENIO/meta2-2
   enabled=true
   start_at_boot=yes
   on_die=respawn
   group=OPENIO,meta2,meta2-2
   uid=openio
   gid=openio
   env.PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin

Create a new configuration file (``meta2-2.yml``) in the ``/etc/oio/sds/OPENIO/watch`` directory:

.. code-block:: shell
   :caption: /etc/oio/sds/OPENIO/watch/meta2-2.yml

   host: 10.0.0.36
   port: 6122
   type: meta2
   location: yb-1
   checks:
   - {type: tcp}
   stats:
   - {type: volume, path: /var/lib/oio/sds/OPENIO/meta2-2}
   - {type: meta}
   - {type: system}

The following configuration must be adapted to your new service:

- host
- port        
- type: volume, path

Then, to make your new meta2 service available, you have to reload the configuration and start the service:

.. code-block:: text

    $ gridinit_cmd reload
    $ gridinit_cmd start OPENIO-meta2-2

And to restart the conscience agent:

.. code-block:: text

    $ gridinit_cmd restart @conscienceagent

Finally, you will have to unlock your new service:

.. code-block:: text

    $ openio cluster unlock meta2 10.0.0.36:6122

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
    | meta2   | 10.0.0.36:6122 | n/a        | /var/lib/oio/sds/OPENIO/meta2-2 | node-1     | n/a   | True |    90 |
    | meta2   | 10.0.0.38:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | node-3     | n/a   | True |    91 |
    | meta2   | 10.0.0.36:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | node-1     | n/a   | True |    90 |
    | meta2   | 10.0.0.37:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | node-2     | n/a   | True |    92 |
    | rawx    | 10.0.0.38:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | node-3     | n/a   | True |    92 |
    | rawx    | 10.0.0.36:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | node-1     | n/a   | True |    90 |
    | rawx    | 10.0.0.37:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | node-2     | n/a   | True |    91 |
    | rdir    | 10.0.0.38:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | node-3     | n/a   | True |    97 |
    | rdir    | 10.0.0.36:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | node-1     | n/a   | True |    95 |
    | rdir    | 10.0.0.37:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | node-2     | n/a   | True |    97 |
    +---------+----------------+------------+---------------------------------+------------+-------+------+-------+
