.. _ref-admin-guide:

==================================
Namespace Configuration (sds.conf)
==================================

Service locations
~~~~~~~~~~~~~~~~~

proxy
-----

Tells the client SDK where is the `oio-proxy` to be used, as the primary
endpoint to the namespace.

.. code-block:: text

    proxy=IP:PORT


conscience
----------

Tells the `oio-proxy` (and only the proxy) where is the `conscience` central
service to be used.

.. code-block:: text

    conscience=IP:PORT[,IP:PORT]*


zookeeper
---------

The ZooKeeper cluster connection string to use for all sqliterepo-based services. Applies to meta0, meta1, meta2 and sqlx services.

.. code-block:: text

    zookeeper=IP:PORT[,IP:PORT]*


zookeeper.$SRVTYPE
------------------

Overrides the global `zookeeper` setting for a specific service type.
In some cases, it is necessary to provide a dedicated ZooKeeper cluster to a service type.
E.g. because it is too critical or space consuming.

.. code-block:: text

    zookeeper.meta0=IP:PORT
    zookeeper.meta1=IP:PORT
    zookeeper.meta2=IP:PORT
    zookeeper.sqlx=IP:PORT

proxy-local
-----------

The optional socket path to connect to the local `oio-proxy`. Used by the C SDK.

.. code-block:: text

    proxy-local=/path/to/proxy.sock


ecd
---

Tells the client SDK where is the `erasure code daemon` that will manage the
complex task of computing the erasure code on the data.

.. code-block:: text

    ecd=IP:PORT


event-agent
-----------

The event-agent connection string to use to produce notifications.
The connection string includes the protocol and the endpoint of the notification backend.
Valid backends are:

* `beanstalkd`: protocol `beanstalk://` (default backend)
* `ZeroMQ`: protocols `ipc://` or `tcp://`.

.. code-block:: text

    # Configuration usiing beanstalkd
    event-agent=beanstalk://IP:PORT

    # Configuration using ZeroMQ
    event-agent=ipc:///path/to/event-agent.sock
    event-agent=tcp://IP:PORT


Other
~~~~~

meta1_digits
------------

Please refer to the section about the sizing considerations.

Set to 4 as a default.

.. code-block:: text

    meta1_digits=0|1|2|3|4


.. include:: variables.rst
