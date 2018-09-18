===========================
Decommission a Rawx Service
===========================

Preparation
~~~~~~~~~~~

Find information about the service you want to decommission.
By running ``openio cluster list rawx`` you will get the list of all Rawx service IDs accompanied by their volume paths.

Lock the score of the targeted rawx service to zero by running ``openio cluster lock rawx <RAWX_ID>``, where RAWX_ID is the network address of the service (ip:port).
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

You can launch decommissioning using a configuration file with ``oio-blob-mover -v <CONFIGURATION FILE>`` (the `-v` is to log to stderr in addition to syslog).

If you don't have a configuration file, you can run ``oio-blob-mover -v --generate-config <FILE> --namespace <NAMESPACE> --volume <VOLUME> --user <USER>``.

The `--generate-config` option is used to generate a configuration file with the namespace, volume, and user specified in the command. If FILE doesn't exist, it will be created; otherwise the file's contents will be deleted and replace by the configuration content.

You can also add an option to on existing configuration file using `--edit-config`.
`--daemon` can be used to run mover as a daemon.
