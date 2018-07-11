=================
Check a directory
=================

Check an OpenIO namespace has been fully deployed. Mostly the directory of
services will be checked.

.. list-table::
   :widths: 20 100

   * - meta0
     - check if meta0 are registred on zookeeper.
   * - meta1
     - check if meta1  are reachable.
   * - dir
     - check if prefix are rechable and same as prefix on meta0, and check if meta1 are registered on meta0
   * - rdir
     - check if all rawx have an associated rdir and check if rdir are up

Preparation
~~~~~~~~~~~

You can check if the services are UP using ``openio cluster list``

Launch check
~~~~~~~~~~~~

Run ``oio-check-directory <NAMESPACE> <ACTION>``. ACTION is a value among meta0, meta1, dir, rdir.

For example you can check meta1 on namespace named OPENIO with:

  .. code-block:: text

    $ oio-check-directory OPENIO meta1

The result can be:

  .. code-block:: text

     07/09/2018 03:11:03 Catalog: Loaded 21 services
     07/09/2018 03:11:03 Catalog: Loaded 21 services
     07/09/2018 03:11:03 All the META1 are alive
     07/09/2018 03:11:03 All the META1 have a positive score

You can use option ``--catalog`` to check if service present in conscience are same as service on catalog
Each line of catalog represent a service and must be formated like ``Type IP PORT``.
You can generate a catalog using ``openio cluster list -c Type -c Addr -f value | tr ':' ' '``
