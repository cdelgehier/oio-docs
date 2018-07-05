======================
Rebuild a volume: meta
======================

This documentation is valid for meta1 and meta2. We use meta{1,2} in the following examples, but you need to replace by meta1 or meta2.

Preparation
~~~~~~~~~~~
First you must run ``gridinit_cmd restart @meta{1,2}``, in this way you can check if meta services are up.
You must wait to have a sufficient score for launch rebuilding.
You can check the score by running ``openio cluster list meta{1,2}``.

Launch rebuilding
~~~~~~~~~~~~~~~~~

You can  launch the rebuild by using the ``oio-meta{1,2}-rebuilder`` tool:

  .. code-block:: console

    # oio-meta{1,2}-rebuilder <NAMESPACE>

Options
~~~~~~~

If you want to have more information about current rebuilding, you can change the report interval using ``--report-interval`` option.
The default value is set to 3600 seconds, but if you want a report every minutes, you must launch rebuilding using ``oio-meta{1,2}-rebuilder --report-interval 60``.

By default, the rebuilding use only one worker, you can give a number of worker using ``--workers`` option.
For example, ``oio-meta{1,2}-rebuilder --workers 42`` launch rebuilding using 42 workers.

The workers have a limited number of prefix to rebuild per seconds, 30 by default: the goal is to keep the meta performance during the rebuiliding.
You can change this value using ``--prefixes-per-seconds`` option. If you want to unlimit the number of prefix to rebuild per seconds,
you can use ``oio-meta{1,2}-rebuilder --prefixes-per-seconds 0``.

If you want to rebuild only some containers you can give a file in argument. This file must contain containers IDs.
The IDs must be formatted like base_name line of ``openio container show <container>``.
For example:

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

The format of the container IDs must be like ``43839DACDD060FA939FAE2714A60640BDC5AFFDDBE8C494BDAB7AA994C3190A5`` for meta2.
For meta1 you can only give prefix. The prefix size is stored on sds.conf (meta1_digits=4).
If your prefix size is 4 you just need to give ``4383`` for example.
