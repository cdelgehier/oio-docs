===========================================
Fix Invalid, Corrupted or Missing Databases
===========================================

The problem
-----------

When you query a specific container, one of the services hosting it
returns an error saying that the database file is missing, or is corrupt, or
has missing entries in its admin table. In such a case, the replication mechanism
should fetch a fresh copy of the database from another peer, but for some
reason, it does not.

  .. code-block:: console

    > openio container show FVE0 --debug
    +----------------+--------------------------------------------------------------------+
    | Field          | Value                                                              |
    +----------------+--------------------------------------------------------------------+
    | account        | myaccount                                                          |
    | base_name      | 697ECB056A5F9339B36C3B0A020B5AB17B4B0160FBEBEA203315EA1FC1B61605.1 |
    | bytes_usage    | 0B                                                                 |
    | container      | FVE0                                                               |
    | ctime          | 1507817632                                                         |
    | max_versions   | Namespace default                                                  |
    | meta.a         | 1                                                                  |
    | objects        | 0                                                                  |
    | quota          | Namespace default                                                  |
    | storage_policy | Namespace default                                                  |
    +----------------+--------------------------------------------------------------------+
    > openio container show FVE0 --debug
    'sys.m2.ctime'
    Traceback (most recent call last):
      File "/usr/lib/python2.7/site-packages/cliff/app.py", line 387, in run_subcommand
        result = cmd.run(parsed_args)
      File "/usr/lib/python2.7/site-packages/cliff/display.py", line 100, in run
        column_names, data = self.take_action(parsed_args)
      File "/home/fvennetier/src/public_git/oio-sds/oio/cli/container/container.py", line 231, in take_action
        ctime = float(sys['sys.m2.ctime']) / 1000000.
    KeyError: 'sys.m2.ctime'
    Exception raised: 'sys.m2.ctime'
    > openio container show FVE0 --debug
    +----------------+--------------------------------------------------------------------+
    | Field          | Value                                                              |
    +----------------+--------------------------------------------------------------------+
    | account        | myaccount                                                          |
    | base_name      | 697ECB056A5F9339B36C3B0A020B5AB17B4B0160FBEBEA203315EA1FC1B61605.1 |
    | bytes_usage    | 0B                                                                 |
    | container      | FVE0                                                               |
    | ctime          | 1507817632                                                         |
    | max_versions   | Namespace default                                                  |
    | meta.a         | 1                                                                  |
    | objects        | 0                                                                  |
    | quota          | Namespace default                                                  |
    | storage_policy | Namespace default                                                  |
    +----------------+--------------------------------------------------------------------+

The solution
------------

Since openio-sds 4.2, it is possible force the synchronization of the base on each
peer by using ``openio election sync`` with the type of service and the name
of the database as parameters.

  .. code-block:: console

    > openio election sync meta2 FVE0
    +----------------+--------+-----------+------+
    | Id             | Status | Message   | Body |
    +----------------+--------+-----------+------+
    | 127.0.0.1:6015 |    200 | OK        |      |
    | 127.0.0.1:6016 |    301 | not SLAVE |      |
    | 127.0.0.1:6017 |    200 | OK        |      |
    +----------------+--------+-----------+------+

Services 127.0.0.1:6015 and 127.0.0.1:6017 have fetched a fresh copy of the
entire database from 127.0.0.1:6016.
