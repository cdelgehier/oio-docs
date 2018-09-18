=======================
Rebuild a Volume: Meta1
=======================

Preparation
~~~~~~~~~~~
First, run ``gridinit_cmd restart @meta1``; this allows you to check that meta services are up.
If scores are low, the rebuilder can take a long time and can fail due to a timeout.
You can check the score by running ``openio cluster list meta1``.

Launch rebuilding
~~~~~~~~~~~~~~~~~

You can  launch the rebuild by using the ``oio-meta1-rebuilder`` tool:

  .. code-block:: console

    # oio-meta1-rebuilder <NAMESPACE>

    14171 7FD246EFC9B0 log INFO RUN worker=0 started=2018-07-10T11:29:02 passes=1 errors=0 meta1_prefixes=1 255.49/s waiting_time=0.00 rebuilder_time=0.00 total_time=0.00 (rebuilder: 100.00%)
    14171 7FD24826BCD0 log INFO DONE started=2018-07-10T11:29:02 ended=2018-07-10T11:29:06 elapsed=3.67 passes=110 errors=0 meta1_prefixes=111 30.21/s waiting_time=1.83 rebuilder_time=1.83 (rebuilder: 100.00%)

Options
~~~~~~~

If you want more information about current rebuilding, you can change the report interval using the ``--report-interval`` option.
The default value is set to 3600 seconds, but if you want a report every minute, you can launch rebuilding using ``oio-meta1-rebuilder --report-interval 60``.

By default, rebuilding uses only one worker; you can set a number of workers using the ``--workers`` option.
For example, ``oio-meta1-rebuilder --workers 42`` launches rebuilding using 42 workers.

Workers have a limited number of prefixes to rebuild per seconds, 30 by default: the goal is to maintain the meta performance during the rebuilding.
You can change this value using the ``--prefixes-per-seconds`` option. If you want to unlimit the number of prefixes to rebuild per second,
you can use ``oio-meta1-rebuilder --prefixes-per-seconds 0``.

If you want to rebuild only some containers, you can specify a file. This file must contain container prefix IDs.
The prefix ID size is stored in sds.conf (meta1_digits=4). You just need to give first digits of base_name line of ``openio container show <container>``.
For example, if you want to rebuuild only container1:

  .. code-block:: console

     # openio container show container1

     +----------------+--------------------------------------------------------------------+
     | Field          | Value                                                              |
     +----------------+--------------------------------------------------------------------+
     | account        | my_account                                                         |
     | base_name      | 43839DACDD060FA939FAE2714A60640BDC5AFFDDBE8C494BDAB7AA994C3190A5.1 |
     | bytes_usage    | 335B                                                               |
     | container      | container1                                                         |
     | ctime          | 1530778169                                                         |
     | max_versions   | Namespace default                                                  |
     | objects        | 2                                                                  |
     | quota          | Namespace default                                                  |
     | status         | Enabled                                                            |
     | storage_policy | Namespace default                                                  |
     +----------------+--------------------------------------------------------------------+

You can specify ``4383`` for the file and launch rebuilding using:

  .. code-block:: console

    # oio-meta1-rebuilder <NAMESPACE> --input-file file
