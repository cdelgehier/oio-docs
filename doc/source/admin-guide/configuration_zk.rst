=============================
Configure a Zookeeper Service
=============================

Description
-----------

This service is used to store directory services election status.

Prerequisites
-------------

Installation
------------

Configuration
-------------

Sample configuration file
-------------------------

.. code-block:: ini
   :caption: /etc/oio/sds/OPENIO/zookeeper-0/zoo.cfg

   # The number of milliseconds of each tick
   tickTime=2000
   # The number of ticks that the initial
   # synchronization phase can take
   initLimit=10
   # The number of ticks that can pass between
   # sending a request and getting an acknowledgement
   syncLimit=5
   # the directory where the snapshot is stored.
   dataDir=/var/lib/oio/sds/OPENIO/zookeeper-0
   # the port at which the clients will connect
   clientPort=6005
   maxClientCnxns=200
   autopurge.snapRetainCount=3
   autopurge.purgeInterval=1

   server.1=172.17.0.2:2888:3888
   server.2=172.17.0.3:2888:3888
   server.3=172.17.0.4:2888:3888
