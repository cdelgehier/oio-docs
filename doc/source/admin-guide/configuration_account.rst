=============================
Configure the account service
=============================

Description
-----------

The account service stores account related information such as the containers list, the number of objects and the number of bytes occupied by all objects.
Following an operation on a container (PUT, DELETE), events are created and consume by the account service in order to update the account information asynchronously.

Prerequisites
-------------

Installation
------------

Configuration
-------------

Sample configuration file
-------------------------

.. code-block:: ini
   :caption: /etc/oio/sds/OPENIO/account-0/account-0.conf

   [account-server]
   bind_addr = 172.17.0.3
   bind_port = 6009
   sentinel_hosts = 172.17.0.2:6012,172.17.0.3:6012,172.17.0.4:6012
   sentinel_master_name = OPENIO-master-1
   log_level = INFO
   log_facility = LOG_LOCAL0
   log_address = /dev/log
   syslog_prefix = OIO,OPENIO,account,0
   autocreate = true
