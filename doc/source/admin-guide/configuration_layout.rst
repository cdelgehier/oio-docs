=================
Filesystem Layout
=================

A standard OpenIO installation deploys its configuration files in locations that
respect `Filesystem Hierarchy standards <http://www.pathname.com/fhs/>`_.

.. contents::
   :depth: 1
   :local:

OpenIO SDS
++++++++++

Here is a sample installation on a node hosting 4 HDDs and 1 SSD. In a
typical deployment, you set up one rawx service per HDD (plus its side services),
1 high-level directory service of each kind (account, meta0, meta1) on the first
SSD, then 4 meta2 services per SSD. All the local stateless services are deployed
once, also on the first SSD.

Data
----

Persistent data resides in the `/var/lib/oio/sds/{NAMESPACE}` directory,
where `{NAMESPACE}` is replaced by the name of the **namespace** being used.

.. code-block:: console

   $ cd /var/lib/oio/sds/NS
   $ find . -type d
   ./coredump
   ./hdd1
   ./hdd1/rawx-1
   ./hdd1/rdir-1
   ./hdd2
   ./hdd2/rawx-2
   ./hdd2/rdir-2
   ./hdd3
   ./hdd3/rawx-3
   ./hdd3/rdir-3
   ./hdd4
   ./hdd4/rawx-4
   ./hdd4/rdir-4
   ./ssd1
   ./ssd1/beanstalkd-1
   ./ssd1/meta0-1
   ./ssd1/meta1-1
   ./ssd1/meta2-1
   ./ssd1/meta2-2
   ./ssd1/meta2-3
   ./ssd1/meta2-4
   ./ssd1/redis-1
   ./ssd1/redissentinel-1

Logs
----

Each service generates an execution journal as well as an access log. The
output is sent through the `/dev/log` device to the local `systemd-journald`
service (we recommend also using `rsyslogd` as a backup). The default
configuration organizes log files per service in the `/var/log/oio/sds/{NAMESPACE}`
directory.

To understand the format of the logs, refer to the dedicated
page :ref:`label-log-format`.

.. code-block:: console

   $ cd /var/log/oio/sds/NS
   $ /bin/ls -1fd *
   account-1
   conscienceagent-1
   memcached-1
   meta0-1
   meta1-1
   meta2-1
   meta2-2
   meta2-3
   meta2-4
   oio-blob-indexer-1
   oio-blob-indexer-2
   oio-blob-indexer-3
   oio-blob-indexer-4
   oio-proxy-1
   rawx-1
   rawx-2
   rawx-3
   rawx-4
   rdir-1
   rdir-2
   rdir-3
   rdir-4
   redis-1
   redissentinel-1


NS Configuration
----------------

The configuration of namespaces, used by services but also by client
applications, resides in the file `/etc/oio/sds.conf` and is superseded by
those found in the `/etc/oio/sds.conf.d` directory.

.. code-block:: console

   $ cd /etc/oio/sds.conf.d/
   $ find .
   NS
   ANOTHER_NS
   YET_ANOTHER_NS


Services configuration
----------------------

The configuration of a service resides in the `/etc/oio/sds/{NAMESPACE}`
directory. At that path, in addition to one directory used to host occasional
core dumps, each partition used by an OIO SDS service is stored.

.. code-block:: console

   $ cd /etc/oio/sds/NS
   $ find .
   ./account-1
   ./beanstalkd-1
   ./conscience-1
   ./conscience-agent-1
   ./memcached-1
   ./meta0-1
   ./meta1-1
   ./meta2-1
   ./meta2-1
   ./meta2-1
   ./meta2-1
   ./oio-blob-indexer-1
   ./oio-blob-indexer-2
   ./oio-blob-indexer-3
   ./oio-blob-indexer-4
   ./oio-event-agent-1
   ./oioproxy-1
   ./rawx-1
   ./rawx-2
   ./rawx-3
   ./rawx-4
   ./rdir-1
   ./rdir-2
   ./rdir-3
   ./rdir-4
   ./redis-1
   ./redissentinal-1
   ./watch


Swift/S3
++++++++

OpenIO FS
+++++++++

Grid For Apps
+++++++++++++
