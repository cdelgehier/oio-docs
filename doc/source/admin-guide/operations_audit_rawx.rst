==========
Audit rawx
==========

The rawx auditor will parse every chunks to detect faulty, corrupted and orphan chunk.

Preparation
~~~~~~~~~~~

Find information about the service you want to audit.
By running ``openio cluster list rawx`` you will get the list of all rawx service ids accompanied by their volume path.

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

Run ``oio-blob-auditor -v <CONFIGURATION FILE>`` (the `-v` is to log to stderr in addition to syslog).


The process does not stop by itself (it was designed as a daemon). Hit Ctrl-C when you don't see any update for 30s.


Audit example
~~~~~~~~~~~~~

The following trace show an audit with an error on chunk position.

  .. code-block:: text

     $ oio-blob-auditor etc/blob-auditor.conf-sample -v
     7371 7FF080B892D0 log INFO Mon Jul  9 10:31:21 2018 1 0 0 0 0 206.31 46213.68 0.00 0.000.00
     7371 7FF080B892D0 log INFO Mon Jul  9 10:31:21 2018 30 0 0 0 0 29.99 4685.07 1.01 0.940.94
     7371 7FF080B892D0 log INFO Mon Jul  9 10:31:22 2018 31 0 0 0 0 30.66 5527.22 2.02 1.990.99
     7371 7FF080B892D0 log INFO Mon Jul  9 10:31:23 2018 31 0 0 0 0 29.36 4757.40 3.07 3.000.98
     7371 7FF080B892D0 log INFO Mon Jul  9 10:31:24 2018 31 0 0 0 0 30.00 4642.73 4.11 4.020.98
     7371 7FF080B892D0 log INFO Mon Jul  9 10:31:25 2018 31 0 0 0 0 30.64 5411.00 5.12 5.070.99
     7371 7FF080B892D0 log INFO Mon Jul  9 10:31:26 2018 30 0 0 0 0 29.37 5140.08 6.14 6.050.98
     7371 7FF080B892D0 log ERROR ERROR faulty chunk .oio/sds/data/OPENIO-rawx-1/F38/F3864ADF8B4F8FDEDE4DADA0A212B4D58B5B01AB1A4D0AFD5BFF34FE8C221BDE: Invalid chunk position found
     7371 7FF080B892D0 log INFO 6.62 0 1 0 0 30.23 5063.08 6.58 0.99
     7371 7FF080B892D0 log INFO Mon Jul  9 10:31:58 2018 1 0 0 0 0 83.19 18633.96 0.01 0.000.00
     7371 7FF080B892D0 log INFO Mon Jul  9 10:31:58 2018 30 0 0 0 0 29.99 4684.20 1.01 0.950.94
     7371 7FF080B892D0 log INFO Mon Jul  9 10:31:59 2018 30 0 0 0 0 30.00 5363.59 2.01 1.940.97
     ...
