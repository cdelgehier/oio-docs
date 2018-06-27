=============
Health checks
=============

This page contains steps to verify the overall health of an OpenIO SDS cluster.

If experiencing issues, use the checks provided below to diagnose any problems.

Environment health
------------------

To verify the end-to-end functionality of an OpenIO SDS cluster, create, download and delete an example object.


1. Create a new container `test` in `health` account:

  .. code-block:: console

    $ openio --oio-account health container create test

  You can check the created container:

  .. code-block:: console

    $ openio --oio-account health container show test

  List containers in account:

  .. code-block:: console

    $ openio --oio-account health container list

2. Create a new object:

  .. code-block:: console

    $ openio --oio-account health object create test /etc/magic

  You can check the created object.

  .. code-block:: console

    $ openio --oio-account health object show test magic

3.  Download the object:

  .. code-block:: console

    $ openio --oio-account health object save test magic --file /tmp/check

  You can check the downloaded object:

  .. code-block:: console

    $ md5sum /etc/magic /tmp/check

4. Once the functionality has been verified, the container and object can be deleted.

  .. code-block:: console

    $ openio --oio-account health object delete test magic
    $ openio --oio-account health container delete test


Host health
-----------

To verify that the cluster is up and running:

  .. code-block:: console

    $ openio cluster list
    +---------+----------------+---------------------------------+---------------+-------+------+-------+
    | Type    | Id             | Volume                          | Location      | Slots | Up   | Score |
    +---------+----------------+---------------------------------+---------------+-------+------+-------+
    | rdir    | 10.0.2.15:6010 | /var/lib/oio/sds/OPENIO/rdir-0  | ubuntu-node1  | n/a   | True |    99 |
    | rdir    | 10.0.2.16:6010 | /var/lib/oio/sds/OPENIO/rdir-0  | ubuntu-node2  | n/a   | True |    99 |
    | rdir    | 10.0.2.17:6010 | /var/lib/oio/sds/OPENIO/rdir-0  | ubuntu-node3  | n/a   | True |    99 |
    | account | 10.0.2.15:6009 | n/a                             | ubuntu-node1  | n/a   | True |    99 |
    | account | 10.0.2.16:6009 | n/a                             | ubuntu-node2  | n/a   | True |    99 |
    | account | 10.0.2.17:6009 | n/a                             | ubuntu-node3  | n/a   | True |    99 |
    | rawx    | 10.0.2.15:6004 | /var/lib/oio/sds/OPENIO/rawx-0  | ubuntu-node1  | n/a   | True |    94 |
    | rawx    | 10.0.2.16:6004 | /var/lib/oio/sds/OPENIO/rawx-0  | ubuntu-node2  | n/a   | True |    94 |
    | rawx    | 10.0.2.17:6004 | /var/lib/oio/sds/OPENIO/rawx-0  | ubuntu-node3  | n/a   | True |    94 |
    | meta2   | 10.0.2.15:6003 | /var/lib/oio/sds/OPENIO/meta2-0 | ubuntu-node1  | n/a   | True |    94 |
    | meta2   | 10.0.2.16:6003 | /var/lib/oio/sds/OPENIO/meta2-0 | ubuntu-node2  | n/a   | True |    94 |
    | meta2   | 10.0.2.17:6003 | /var/lib/oio/sds/OPENIO/meta2-0 | ubuntu-node3  | n/a   | True |    94 |
    | meta1   | 10.0.2.15:6002 | /var/lib/oio/sds/OPENIO/meta1-0 | ubuntu-node1  | n/a   | True |    94 |
    | meta1   | 10.0.2.16:6002 | /var/lib/oio/sds/OPENIO/meta1-0 | ubuntu-node2  | n/a   | True |    94 |
    | meta1   | 10.0.2.17:6002 | /var/lib/oio/sds/OPENIO/meta1-0 | ubuntu-node3  | n/a   | True |    94 |
    | meta0   | 10.0.2.15:6001 | /var/lib/oio/sds/OPENIO/meta0-0 | ubuntu-node1  | n/a   | True |    99 |
    | meta0   | 10.0.2.16:6001 | /var/lib/oio/sds/OPENIO/meta0-0 | ubuntu-node2  | n/a   | True |    99 |
    | meta0   | 10.0.2.17:6001 | /var/lib/oio/sds/OPENIO/meta0-0 | ubuntu-node3  | n/a   | True |    99 |
    +---------+----------------+---------------------------------+---------------+-------+------+-------+

The above cluster example shows three hosts running. All services are up and scores are greater than 0.

All hosts in the cluster should be visible in the output.

**Processes**

To verify all processes are up and running, use `gridinit_cmd`:

  .. code-block:: console

    $ gridinit_cmd status
    KEY                       STATUS      PID GROUP
    OPENIO-account-0          UP         1141 OPENIO,account,account-0
    OPENIO-beanstalkd-0       UP         1123 OPENIO,beanstalkd,beanstalkd-0
    OPENIO-conscience-0       UP         1116 OPENIO,conscience,conscience-0
    OPENIO-conscienceagent-0  UP         1140 OPENIO,conscienceagent,conscienceagent-0
    OPENIO-meta0-0            UP         1119 OPENIO,meta0,meta0-0
    OPENIO-meta1-0            UP         1135 OPENIO,meta1,meta1-0
    OPENIO-meta2-0            UP         1114 OPENIO,meta2,meta2-0
    OPENIO-oio-blob-indexer-0 UP         1118 OPENIO,oio-blob-indexer,oio-blob-indexer-0
    OPENIO-oio-event-agent-0  UP         1121 OPENIO,oio-event-agent,oio-event-agent-0
    OPENIO-oioproxy-0         UP         1117 OPENIO,oioproxy,oioproxy-0
    OPENIO-rawx-0             UP         1132 OPENIO,rawx,rawx-0
    OPENIO-rdir-0             UP         1133 OPENIO,rdir,rdir-0
    OPENIO-redis-0            UP         1120 OPENIO,redis,redis-0
    OPENIO-redissentinel-0    UP         1136 OPENIO,redissentinel,redissentinel-0
    OPENIO-zookeeper-0        UP         1138 OPENIO,zookeeper,zookeeper-0


All processes should be marked as `UP`.

**Redis**

TODO

**ZooKeeper**

A basic ZooKeeper health check can be done with:

  .. code-block:: console

    $ echo ruok | nc 10.0.2.15 6005
    imok

  Retrieve the correct ip and port for ZooKeeper in `/etc/oio/sds.conf.d/NAMESPACE`.

To get more information about the ZooKeeper cluster:

  .. code-block:: console

    $ echo stats | nc 10.0.2.15 6005
    Zookeeper version: 3.4.10-2oio--1, built on Thu, 05 Oct 2017 15:55:37 +0000
    Clients:
     /10.0.2.15:48488[1](queued=0,recved=401,sent=401)
     /10.0.2.15:48486[1](queued=0,recved=401,sent=401)
     /10.0.2.15:48490[1](queued=0,recved=401,sent=401)
     /10.0.2.15:48418[1](queued=0,recved=404,sent=404)
     /10.0.2.15:44918[0](queued=0,recved=1,sent=0)

    Latency min/avg/max: 0/0/10
    Received: 1608
    Sent: 1607
    Connections: 5
    Outstanding: 0
    Zxid: 0x2127d
    Mode: standalone
    Node count: 135695

**Storage**

Check disk usage of a host using `df`:

  .. code-block:: console

    $ df -hT

Services stores their data in `/var/lib/oio`.
