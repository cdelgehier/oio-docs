=============================
Monitor an OpenIO SDS cluster
=============================

Introduction
------------

This document will help you to configure a monitoring stack for your
OpenIO cluster.


We use Netdata for local system monitoring, OpenIO processes and
OpenIO basic log analysis and Diamond for OpenIO services informations.
It will be totally replaced by Netdata is the next releases. Netdata
collect metrics and allows you to see, for each node, the last data of
your node during the last hour with high precision (1 second).

Netdata will be configured to send metrics to InfluxDB which collects
all metrics from all nodes, and a Grafana dashboard will allow you to
see your cluster global metrics.

This document will help you setup your admin server and all nodes
accordingly.

Admin
-----

InfluxDB
~~~~~~~~

We use InfluxDB to store the OpenIO cluster metrics. Netdata and
Diamond are configured to send metrics every 10 seconds, we recommend
that the node hosting this service should have at 8GB of RAM and 4 CPU
cores with 120GB of SSD available for a small setup.
Please refer to `InfluxDB hardware sizing for more
informations <https://docs.influxdata.com/influxdb/v1.2/guides/hardware_sizing/>`__.

Install
^^^^^^^

Depending on the distribution you are using, `install InfluxDB from the
official repository <https://portal.influxdata.com/downloads>`__.

Configure
^^^^^^^^^

Netdata and Diamond will send metrics through InfluxDB input plugin. A
template will convert Graphite style strings to InfluxDB tags.

In the InfluxDB configuration file ``/etc/influxdb/influxdb.conf``,
your ``[[graphite]]`` block should have this informations:

::

    [[graphite]]
      enabled = true
      database = "graphite"
      separator = "_"
      templates = [
        "servers.*.cpu.* .host.measurement.cpu.measurement* resource=cpu",
        "servers.*.diskspace.* .host.measurement.label.measurement* resource=diskspace",
        "servers.*.iostat.* .host.measurement.device.measurement* resource=iostat",
        "servers.*.network.* .host.measurement.device.measurement* resource=network",
        "servers.*.loadavg.* .host.measurement* resource=loadavg",
        "servers.*.memory.* .host.measurement* resource=memory",
        "servers.*.vmstat.* .host.measurement* resource=vmstat",
        "servers.*.netstat.* .host.measurement* resource=netstat",
        "servers.*.tcp.* .host.measurement* resource=tcp",
        "servers.*.openio.*.*.*.*.byte_percentfree .host.measurement.namespace.service_type.service_id.blk_uuid.measurement*",
        "servers.*.openio.*.*.*.*.byte_avail .host.measurement.namespace.service_type.service_id.blk_uuid.measurement*",
        "servers.*.openio.*.*.*.*.byte_free .host.measurement.namespace.service_type.service_id.blk_uuid.measurement*",
        "servers.*.openio.*.*.*.*.byte_used .host.measurement.namespace.service_type.service_id.blk_uuid.measurement*",
        "servers.*.openio.*.beanstalkd.*.tubes.*.* .host.measurement.namespace.measurement.service_id.measurement.tube.type",
        "servers.*.openio.*.beanstalkd.*.* .host.measurement.namespace.measurement.service_id.measurement*",
        "servers.*.openio.*.zookeeper.*.* .host.measurement.namespace.measurement.service_id.measurement*",
        "servers.*.openio.*.redis.*.* .host.measurement.namespace.measurement.service_id.measurement*",
        "servers.*.openio.*.*.*.*.*.* .host.measurement.namespace.service_type.service_id.measurement.measurement.type",
        "servers.*.openio.*.*.*.*.* .host.measurement.namespace.service_type.service_id.measurement*",
        "servers.*.openio.*.*.*.* .host.measurement.namespace.service_type.service_id.measurement*",
        "netdata.*.system.ctxt.* .host..measurement.measurement",
        "netdata.*.system.cpu.* .host..measurement.mode cpu=system",
        "netdata.*.system.forks.started .host..measurement.type",
        "netdata.*.system.io.* .host.disk.measurement.operation measurement=disk",
        "netdata.*.system.processes.* .host..measurement.type",
        "netdata.*.system.ram.* .host..measurement.type",
        "netdata.*.system.load.* .host..measurement.avg",
        "netdata.*.system.uptime.uptime .host...measurement",
        "netdata.*.cpu.*.* .host.measurement.cpu.mode",
        "netdata.*.disk.*.* .host.measurement.disk.operation",
        "netdata.*.disk_backlog.*.* .host.measurement.disk.operation",
        "netdata.*.disk_util.*.* .host.measurement.disk.",
        "netdata.*.disk_inodes.*.* .host.measurement.mountpoint.type",
        "netdata.*.disk_ops.*.* .host.measurement.disk.operation",
        "netdata.*.disk_space.*.* .host.measurement.mountpoint.type",
        "netdata.*.mem.*.* .host.measurement.measurement.type",
        "netdata.*.net.*.* .host.measurement.iface.type",
        "netdata.*.net_drops.*.* .host.measurement.iface.type",
        "netdata.*.net_packets.*.* .host.measurement.iface.type",
        "netdata.*.ipv4.errors.* .host.measurement.measurement.type",
        "netdata.*.ipv4.tcpsock.* .host.measurement.measurement.type",
        "netdata.*.ipv4.tcppackets.* .host.measurement.measurement.type",
        "netdata.*.ipv4.tcperrors.* .host.measurement.measurement.type",
        "netdata.*.ipv4.tcphandshake.* .host.measurement.measurement.type",
        "netdata.*.ipv4.udppackets.* .host.measurement.measurement.type",
        "netdata.*.ipv4.packets.* .host.measurement.measurement.type",
        "netdata.*.apps.cpu.openio.* .host...measurement.servicetype resource=cpu,mode=used",
        "netdata.*.apps.cpu_system.openio.* .host...measurement.servicetype resource=cpu,mode=system",
        "netdata.*.apps.cpu_user.openio.* .host...measurement.servicetype resource=cpu,mode=user",
        "netdata.*.apps.preads.openio.* .host...measurement.servicetype resource=disk,type=read",
        "netdata.*.apps.pwrites.openio.* .host...measurement.servicetype resource=disk,type=write",
        "netdata.*.apps.files.openio.* .host...measurement.servicetype resource=files",
        "netdata.*.apps.mem.openio.* .host...measurement.servicetype resource=mem",
        "netdata.*.apps.vmem.openio.* .host...measurement.servicetype resource=vmem",
        "netdata.*.apps.processes.openio.* .host...measurement.servicetype resource=processes",
        "netdata.*.apps.threads.openio.* .host...measurement.servicetype resource=threads",
        "netdata.*.apps.pipes.openio.* .host...measurement.servicetype resource=pipes",
        "netdata.*.apps.sockets.openio.* .host...measurement.servicetype resource=sockets",
        "netdata.*.web_log_.openio.*.*.*.log.* .host..measurement.namespace.servicetype.serviceid.measurement..measurement.type",
      ]

You can now start and enable InfluxDB::

# systemctl enable influxdb
# systemctl start influxdb

Authentication
^^^^^^^^^^^^^^

We recommend you to setup at least an authentication to your InfluxDB
and/or to make the service listen only on a private IP.
Let's create a root user to access to the HTTP API of InfluxDB.
Connect to InfluxDB through the command line as follows::

# influx -execute "CREATE USER admin WITH PASSWORD '<password>' WITH ALL PRIVILEGES"

Then in your ``/etc/influxdb/influxdb.conf`` configuration file, in the
``[http]`` block, enable authentication::

    auth-enabled = true

And restart InfluxDB::

# systemctl restart influxdb

For more informations, please refer to the `InfluxDB
documentation <https://docs.influxdata.com/influxdb/v1.2/query_language/authentication_and_authorization/>`__.

Grafana
~~~~~~~

Install
^^^^^^^

Same goes for Grafana, available from the `Grafana download
page <https://grafana.com/grafana/download>`__.

Configure
^^^^^^^^^

Start Grafana and follow the install guide from the Web interface::

# systemctl enable grafana-server
# systemctl start grafana-server

Using your Web browser, connect to the admin node and configure an
InfluxDB Data Source.

Name it ``InfluxDB`` to match the dashboard name we provide, here are
the other informations::

    Name: InfluxDB
    Type: InfluxDB

    Http settings
    Url: http://localhost:8086/
    Access: proxy

    Http Auth
    Basic Auth: True

    InfluxDB Details
    Database: graphite
    User: admin
    Password: <password>

    Default group by time: >10s

Then press ``Save & Test`` and your Data Source is configured.

Dashboard
^^^^^^^^^

We provide an OpenIO dashboard to monitor your cluster. To import it,
in ``Dashbords``, press ``Import``.

Copy/paste the content of the `OpenIO
dashboard <https://raw.githubusercontent.com/open-io/grafana-dashboards/master/openio.json>`__
in the corresponding field and press ``Import``.

For the Grafana templating to work, click on the wheel on the top of
the page (alt informations is ``Manage dashboard``) then press
``Templating``. On each ``host`` and ``namespace`` line, press ``Edit``
and in the bottom of the page, press ``Update``. This part will update
the templating informations allowing you to select only one or more host
and or namespace to show.

You will need to redo this part after configuring your nodes.

Node
----

Netdata
~~~~~~~

Install
^^^^^^^

Netdata package is available in OpenIO repository, depending on the
distribution you use, install the package on each node by using::

# yum install netdata
# apt-get install netdata

Configure
^^^^^^^^^

In ``/etc/netdata/netdata.conf``, configure your InfluxDB server. At the
end of the file, add thos block and be sure to replace
``INFLUXDB_IPADDR`` by your admin node IP address::

    [backend]
      enabled = yes
      type = graphite
      destination = INFLUXDB_IPADDR
      data source = average
      # prefix = netdata
      # hostname = HOSTNAME
      update every = 10
      buffer on failures = 10
      timeout ms = 20000

On top of the ``/etc/netdata/apps_groups.conf`` file, add the following
lines::

    openio.account: oio-account-ser
    openio.beanstalkd: *beanstalkd-*
    openio.conscienceagent: *conscienceagent-*
    openio.conscience: *conscience-*
    openio.ecd: *ecd-*
    openio.meta0: oio-meta0-serve
    openio.meta1: oio-meta1-serve
    openio.meta2: oio-meta2-serve
    openio.blob-indexer: oio-blob-indexe
    openio.event-agent: oio-event-agent
    openio.oio-proxy: oio-proxy
    openio.rawx: *rawx-*
    openio.rdir: oio-rdir-server
    openio.redis: *redis-*
    openio.redissentinel: *redissentinel-*
    openio.zookeeper: *zookeeper-*

In the ``/etc/netdata/python.d.conf`` file, be sure the ``web_log``
plugin is enabled::

    web_log: yes

For each OpenIO RAW-X service configured on your server, add the
following lines to the ``/etc/netdata/python.d/web_log.conf``, replacing
the ``<NAMESPACE>`` and ``<ID>``::

    <NAMESPACE>-rawx-<ID>:
      name: '.openio.<NAMESPACE>.rawx.rawx-<ID>.log.access'
      path: '/var/log/oio/sds/<NAMESPACE>/rawx-<ID>/rawx-<ID>-httpd-access.log'
      custom_log_format:
        pattern: '\S+ \S+ \S+ \S+ \S+ \d+ \d+ \S+ \S+ (?P<address>\S+) \S+ (?P<method>\S+) (?P<code>\d+) (?P<resp_time>\d+) (?P<bytes_sent>\d+) \S+ \S+ (?P<url>.*)'

For each OpenIO directory service configured on your server, add the
following lines to the ``/etc/netdata/python.d/web_log.conf``, replacing
the ``<NAMESPACE>``, ``<SERVICETYPE>`` (one of ``meta0``, ``meta1`` or
``meta2``) and the service ``<ID>``::

    <NAMESPACE>-<SERVICETYPE>-<ID>:
      name: '.openio.<NAMESPACE>.<SERVICETYPE>.<SERVICETYPE>-<ID>.log.access'
      path: '/var/log/oio/sds/<NAMESPACE>/<SERVICETYPE>-<ID>/<SERVICETYPE>-<ID>.access'
      custom_log_format:
        pattern: '\S+ \S+ \S+ \S+  \S+ \S+ \S+ \S+ (?P<address>\S+) \S+ (?P<method>\S+) (?P<code>\d+) (?P<resp_time>\d+) (?P<bytes_sent>\d+) \S+ \S+ \S+ (?P<url>.*)'

Then enable and restart Netdata::

# systemctl enable netdata
# systemctl restart netdata

Diamond
~~~~~~~

Install
^^^^^^^

Configure
^^^^^^^^^

``/etc/diamond/diamond.conf``

::

    [server]
    handlers = diamond.handler.graphite.GraphiteHandler
    user = root
    group = root
    pid_file = /run/diamond.pid
    collectors_path = /usr/share/diamond/collectors/
    collectors_config_path = /etc/diamond/collectors
    handlers_config_path = /etc/diamond/handlers
    handlers_path = /usr/share/diamond/handlers/
    metric_queue_size = 65536
    [collectors]
    [[default]]
    interval=10

    [handlers]
    keys = rotated_file
    [[default]]

    [loggers]
    keys=root

    [formatters]
    keys=default

    [logger_root]
    handlers=rotated_file
    logger=INFO
    propagate=1

    [handler_rotated_file]
    args=('/var/log/diamond/diamond.log', 'midnight', 1, 7)
    class=handlers.TimedRotatingFileHandler
    formatter=default
    level=INFO

    [formatter_default]
    datefmt=
    format=[%(asctime)s] [%(threadName)s] %(message)s

Configure Diamond to send metrics to your admin node. Replace
``<ADMIN_ADDR>`` by the IP address of your admin node:

``/etc/diamond/handlers/GraphiteHandler.conf``

::

    #[[GraphiteHandler]]
    enabled = true
    host = <ADMIN_IPADDR>
    port = 2003
    timeout = 10
    batch = 1000

Configure the following files, replace and by your namespace name and
the IP address of you node:

``/etc/diamond/collectors/OpenioBeanstalkdCollector.conf``

::

    #[[OpenioBeanstalkdCollector]]
    enabled = true
    instances = <NAMESPACE>:<IPADDR>:6014

``/etc/diamond/collectors/OpenioRedisCollector.conf``

::

    #[[OpenioRedisCollector]]
    enabled = true
    instances = <NAMESPACE>:<IPADDR>:6011

``/etc/diamond/collectors/OpenIOSDSCollector.conf``

::

    #[[OpenIOSDSCollector]]
    enabled = true
    namespaces = <NAMESPACE>
    fs-types =

``/etc/diamond/collectors/OpenioZookeeperCollector.conf``

::

    #[[OpenioZookeeperCollector]]
    enabled = true
    instances = <NAMESPACE>:<IPADDR>:6005


Diamond is now configured, enable and restart it::

# systemctl enable diamond
# systemctl start diamond

End
---

Your monitoring is now available.
Your global OpenIO dashboard is available connecting to
``http://<ADMIN_IPADDR>/dashboard/db/OpenIO`` using the credentials you
set earlier.
