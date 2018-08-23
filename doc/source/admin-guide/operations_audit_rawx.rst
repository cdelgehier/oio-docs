==========
Audit Rawx
==========

The rawx auditor parses every chunk to detect faulty, corrupted, and orphaned chunks.

Preparation
~~~~~~~~~~~

Find information about the service you want to audit.
By running ``openio cluster list rawx`` you will get the list of all rawx service ids accompanied by their volume paths.

Configuration
~~~~~~~~~~~~~

Create a configuration file with the following template:

  .. code-block:: text

     [blob-auditor]
     namespace = <YOUR NAMESPACE NAME>

     # Run daemon as user
     user = openio

     # Volume to audit
     volume = <VOLUME PATH>

     # Report interval (in seconds)
     #report_interval = 3600

     # Throttle: max bytes per second
     #bytes_per_second = 100000000

     # Throttle: max chunks per second
     #chunks_per_second = 30

     # Logging configuration
     #log_level = INFO
     #log_facility = LOG_LOCAL0
     #log_address = /dev/log
     #syslog_prefix = OIO,OPENIO,blob-auditor,1

Launch audit
~~~~~~~~~~~~

You can lauch audit using configuration file with ``oio-blob-auditor -v <CONFIGURATION FILE>`` (the `-v` is to log to stderr in addition to syslog).

If you don’t have configuration file you can run ``oio-blob-auditor -v --generate-config <FILE> --namespace <NAMESPACE> --volume <VOLUME> --user <USER>``

The ``--generate-config`` is to generate configuration file with namespace, volume and user given. If FILE don’t exist, it will be created, else, file content will be deleted and replace by configuration.

You can also add option on existing configuration file using ``--edit-config option``. ``--daemon`` option can be used to run auditor as daemon


Audit example
~~~~~~~~~~~~~

The following trace shows an audit with an error in chunk position.

  .. code-block:: text

     $ oio-blob-auditor auditor.cfg --generate-config --user username --namespace OPENIO --volume /home/username/.oio/sds/data/OPENIO-rawx-1 -v
     28501 7FC0AB241050 log ERROR ERROR faulty chunk /home/username/.oio/sds/data/OPENIO-rawx-1/BC0/BC0140B5701B99946828CB23CB32C5DEDA77E2575A50854D618F0228B3385DAF: Invalid chunk position found
     28501 7FC0AB241050 log INFO Thu Aug 16 12:09:42 2018 1 0 1 0 0 240.26 23786.22 0.00 0.000.00
     28501 7FC0AB241050 log INFO 0.07 0 1 0 0 42.16 4174.28 0.07 1.00
     28501 7FC0AB241050 blob-auditor INFO Daemon exited
