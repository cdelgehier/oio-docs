===========================
Decommission a rawx service
===========================

Preparation
~~~~~~~~~~~

Find information about the service you want to decommission.
By running ``openio cluster list rawx`` you will get the list of all rawx service ids accompanied by their volume path.

Lock the score of the targeted rawx service to zero by running ``openio cluster lock rawx <RAWX_ID>``. Where RAWX_ID is the network address of the service (ip:port).
This will prevent the service from getting upload requests, and will reduce the number of download requests.

Verify that the service is actually locked by running ``openio cluster list rawx`` again.

Configuration
~~~~~~~~~~~~~

Create a configuration file with the following template:

  .. code-block:: text

     [blob-mover]
     namespace = <YOUR NAMESPACE NAME>

     # Run daemon as user
     user = openio

     # Logging configuration
     #log_level = INFO
     #log_facility = LOG_LOCAL0
     #log_address = /dev/log
     #syslog_prefix = OIO,OPENIO,blob-mover,1

     # Volume to move
     volume = <VOLUME PATH>

     # Disk usage target (in percent)
     #usage_target = 0

     # Disk usage check interval (in seconds)
     #usage_check_interval = 3600

     # Report interval (in seconds)
     #report_interval = 3600

     # Throttle: max bytes per second
     #bytes_per_second = 100000000

     # Throttle: max chunks per second
     #chunks_per_second = 30

Launch decommissioning
~~~~~~~~~~~~~~~~~~~~~~

Run ``oio-blob-mover -v <CONFIGURATION FILE>`` (the `-v` is to log to stderr in addition to syslog).

The process does not stop by itself (it was designed as a daemon). Hit Ctrl-C when you don't see any update for 30s.
