=======================
Rebuild a Volume: Meta2
=======================

.. contents::
   :backlinks: none
   :depth: 1
   :local:

Preparation
~~~~~~~~~~~

First, run ``gridinit_cmd restart @meta2``; this allows you to check if meta services are up.
If scores are low, the rebuilder can take a long time and can fail due to a timeout.
You can check the score by running ``openio cluster list meta2``.

Launch rebuilding
~~~~~~~~~~~~~~~~~

You can  launch the rebuild by using the ``oio-meta2-rebuilder`` tool:

  .. code-block:: console

    # oio-meta2-rebuilder <NAMESPACE>

    16479 7F0E45D504B0 log INFO START volume=None last_report=2018-09-18T11:19:18 0.00s references=0 0.00/s errors=0 0.00% start_time=2018-09-18T11:19:18 0.00s total_references=0 0.00/s total_errors=0 0.00%
    16479 7F0E43CCE7D0 log INFO RUN volume=None last_report=2018-09-18T11:19:18 10.01s references=553 55.27/s errors=0 0.00% start_time=2018-09-18T11:19:18 10.01s total_references=553 55.27/s total_errors=0 0.00%
    16479 7F0E45D504B0 log INFO DONE volume=None last_report=2018-09-18T11:19:28 9.68s references=427 44.12/s errors=0 0.00% start_time=2018-09-18T11:19:18 19.68s total_references=980 49.79/s total_errors=0 0.00%

Options
~~~~~~~

If you want to have more information about current rebuilding, you can change the report interval using ``--report-interval`` option.
The default value is set to 3600 seconds, but if you want a report every minutes, you must launch rebuilding using ``oio-meta2-rebuilder --report-interval 60``.

If you want more information about current rebuilding, you can change the report interval using the ``--report-interval`` option.
The default value is set to 3600 seconds, but if you want a report every minute, you can launch rebuilding using ``oio-meta2-rebuilder --report-interval 60``.

By default, the rebuilding use only one worker, you can give a number of worker using ``--workers`` option.
For example, ``oio-meta2-rebuilder --workers 42`` launch rebuilding using 42 workers.

The workers have a limited number of prefix to rebuild per seconds, 30 by default: the goal is to keep the meta performance during the rebuiliding.
You can change this value using ``--prefixes-per-seconds`` option. If you want to unlimit the number of prefix to rebuild per seconds,
you can use ``oio-meta2-rebuilder --prefixes-per-seconds 0``.

If you want to rebuild only some containers you can give a file in argument.
The base_name line of ``openio container show <container>`` is composed by {id}.{seq}.
You just need to give the id part on the file.
For example if you want to rebuild only this container:

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


You specify ``43839DACDD060FA939FAE2714A60640BDC5AFFDDBE8C494BDAB7AA994C3190A5`` as the file and launch rebuilding using:

  .. code-block:: console

    # oio-meta2-rebuilder <NAMESPACE> --input-file file
