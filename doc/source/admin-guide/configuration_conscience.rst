=================================
Configure the conscience services
=================================




Persist conscience service status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Case of use
-----------
You can add an option to add persistence for conscience services status.

The goal of this persistence is to unlock services known before restarting conscience, making openio cluster unlockall not necessary.
New services added while stopped conscience will still requires manual unlock operation.



Enable persistence
------------------

You must specify the file path to used for persistence. The services status are written on this file
and the conscience read it at restart to know what services was enable before conscience stop.

You can get the conscience command using ``gridinit_cmd status2 @conscience``.

To enable persistence launch:

  .. code-block:: console

     # oio-daemon <conscience configuration path> -O PersistencePath=<persistence file path>

The status are written every 30 seconds by default but you can change this value with option ``-O PersistencePeriod=N`` with N the period in seconds.

