=============
Core concepts
=============


Data organisation
~~~~~~~~~~~~~~~~~

.. image:: ../../../images/openio-arch-data-organization.png
   :align: center
   :width: 250 px

Namespace
---------

A coherent set of network services working together to run OpenIO's solutions.

Account
-------
Usually represents a customer (the second 'B' in B2B2C). There is
no limit to the number of accounts in a namespace. Accounts keep track of
namespace usage of each customer (e.g. the list of containers and
the number of bytes occupied by all objects of a customer).

Containers
----------
Object buckets. They keep track of object locations.
A container belongs to one (and only one) account.

TODO More details in `Object Storage`_ section.

Objects
-------
The smallest data units visible by customers. An object belongs
to one (and only one) container.


Chunks
------
Parts of objects, not visible by customers. They are limited in size.
They can be replicated or be accompanied by parity chunks.

.. image:: ../../../images/openio-arch-object-split-in-chunk.png
   :width: 800 px
   :align: center


Container & chunk isolation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each container is stored in a separate file (i.e. not in one unique data structure), and each chunk is also stored as a file. This greatly improves the overall robustness of the solution, and limits the impact of corruption or the loss of a single item.


Massively distributed three-level directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Containers and objects are stored in a persistent three-level distributed directory (Meta-0, Meta-1, Meta-2). OpenIO SDS can store hundreds of services for each of hundred of millions of containers, with strong consistency and low latency, especially for read operations.
The directory has the form of a hash table, mapping containers’ UUIDs to their services. To handle a large number of items, a first level of indirection splits the hash table into 64k slots. Every level is synchronously replicated.
Higher levels of the directory (indirection tables) are particularly stable, and benefit from cache mechanisms in place. Caches are implemented everywhere, especially inside directory gateways, and are also available on the client side.

.. image:: ../../../images/openio-arch-directory-indirection-tables.png
   :width: 600 px
   :align: center

Conscience: dynamic load-balancing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For data placement, OpenIO SDS provides a system called Conscience, responsible for efficiently matching requests and services. Conscience takes into account constraints set by the request (e.g. respect of storage policies) and computes a quality score (between 0 and 100) for each service available in the cluster. These quality scores are based on an algorithm that takes into account several sensors providing data from the nodes of the grid. Through this feedback loop, each node knows in real time which are the best nodes with the highest scores to handle subsequent requests.

A score of 0 indicates the service must be avoided. A positive score means the service can be used, the bigger it is, the best the quality will be.

.. image:: ../../../images/openio-arch-conscience-feedback-loop.png
   :width: 600 px
   :align: center

Reverse directory
~~~~~~~~~~~~~~~~~

The rdir services keep a trace of all chunks stored on each rawx service. When a rawx is broken, admins can rebuild lost chunks thanks to rdir informations assuming that each chunk is duplicated.
When a chunks is uploaded to a rawx (or deleted), this rawx sends an event to the event agent which updates rdir informations.

For each chunk, rdir stores:

- ‘mtime’: date of the last update of this entry (when a chunk is uploaded to a rawx)
- ‘rtime’: date of the rebuilt or not present
- extended attributes of the chunk

If the volume has no associated rdir, a rdir will be automatically associated to
it. The meta1 stores this association using the special account _RDIR.


Metadata proxy
~~~~~~~~~~~~~~
Whichever protocol is in used by the internal services (directories), all clients rely on a layer of gateways that provides a simple REST API for metadata accesses. This API provides high-level operations that encapsulate all the underlying logic behind the management of accounts, containers, and their contents. Gateways are also the ideal place for shared cache mechanisms, similar to the way name service cache daemon works on Linux hosts.

.. image:: ../../../images/openio-client-with-proxy.svg
   :width: 500 px
   :align: center
