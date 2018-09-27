============
Rdir Service
============

Description
-----------

Rdir is a reverse directory that stores chunk references of a rawx. This service is useful to rebuild a rawx.
Each rawx has an Rdir instance associated that is not hosted on the same server.

Prerequisites
-------------

Installation
------------

Configuration
-------------

Sample configuration file
-------------------------

.. code-block:: ini
   :caption: /etc/oio/sds/OPENIO/rdir-0/rdir-0.conf

   [rdir-server]
   bind_addr = 172.17.0.2
   bind_port = 6301
   namespace = OPENIO
   # Currently, only 1 worker is allowed to avoid concurrent access to leveldb database
   workers = 1
   worker_class = sync
   threads = 1
   db_path= /var/lib/oio/sds/OPENIO/rdir-0
   log_facility = LOG_LOCAL0
   log_level = info
   log_address = /dev/log
   syslog_prefix = OIO,OPENIO,rdir,0
