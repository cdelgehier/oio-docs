=================
Check a Directory
=================

Check that an OpenIO namespace has been fully deployed. This checks the directory of services.

.. list-table::
   :widths: 20 100

   * - meta0
     - Check that meta0 services are registered on zookeeper.
   * - meta1
     - Check that meta1 services are reachable.
   * - dir
     - Check that prefixes are reachable and are the same as prefixes on meta0, and check if meta1 services are registered on meta0.
   * - rdir
     - Check that all rawx services have associated rdir and check that rdir are up.

Preparation
~~~~~~~~~~~

You can check if services are UP using ``openio cluster list``

Launch check
~~~~~~~~~~~~

Run ``oio-check-directory <NAMESPACE> <ACTION>``. ACTION is a value among meta0, meta1, dir, rdir.

For example you can check meta1 on the namespace named OPENIO with:

  .. code-block:: text

    $ oio-check-directory OPENIO meta1

The result can be:

  .. code-block:: text

     07/09/2018 03:11:03 Catalog: Loaded 21 services
     07/09/2018 03:11:03 Catalog: Loaded 21 services
     07/09/2018 03:11:03 All the META1 are alive
     07/09/2018 03:11:03 All the META1 have a positive score

You can use the option ``--catalog`` to check if services present in conscience are the same as services in catalog.
Each line of catalog represents a service and must be formatted like ``Type IP PORT``.
You can generate a catalog using ``openio cluster list -c Type -c Addr -f value | tr ':' ' '``
