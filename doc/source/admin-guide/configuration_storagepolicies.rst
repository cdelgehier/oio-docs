========================
Declare Storage Policies
========================

Storage policies are the way to define different storage tiers in your platform.

Each storage policy must at least contain a data security policy and can be used to target only certain pools.

Storage policies are defined for the Conscience service, and are thus available at the namespace level.

.. note::

   By default, the configuration file can be found at /etc/oio/sds/[NS]/conscience-X/conscience-X-policies.conf

Configuration
-------------

Suppose you have configured the following pool in /etc/oio/sds/[NS]/conscience-X/conscience-X-services.conf

.. code-block:: text

    [pool:rawx21]
    targets=2,rawx-site1,rawx;1,rawx-site2,rawx


You can then define a storage policy that uses this pool to replicate chunks 3 times on 2 different sites following the 2+1 model.

.. code-block:: text

    [STORAGE_POLICIES]
    DUPONETHREE=NONE:THREECOPIES
    DUPONETHREE_MULTISITE=rawx21:THREECOPIES


As shown in the example above, a custom storage policy has been created for multi-site replication.

See also :ref:`label-arch-conscience`, :ref:`label-arch-dynstgpol`.

Data Security
-------------

Data security describes the way an object is stored in the storage pool.

Each data security policy is derived from one of the supported security types. For the moment, these are:

* ``plain``: replication security (replicated data chunks).

* ``ec``: erasure coding security (data chunks + parity chunks).

By default, there are 3 data security policies available:

.. code-block:: text

    [DATA_SECURITY]
    THREECOPIES=plain/distance=1,nb_copy=3
    TWOCOPIES=plain/distance=1,nb_copy=2
    ERASURECODE=ec/k=6,m=3,algo=liberasurecode_rs_vand,distance=1

The policies defined above can be interpreted as the following:

- 2 replication policies (THREECOPIES/TWOCOPIES for 2x/3x replication).
- a 6+3 Erasure Coding policy (6 data chunks + 3 parity chunks using Reed Solomon with liberasurecode).

You can add more data security policies on top of the existing ones, or even alter the ones provided by default.
Please note that it is not recommended to alter a data security entry after objects have already been created using
the corresponding Storage Policy, as it may result in data loss.

.. list-table:: Options
   :header-rows: 1

   * - Option
     - Description
   * - ``nb_copy``
     - replication only: defines the number of copies to store.
   * - ``distance``
     - defines the minimum distance between chunks to ensure security.
   * - ``algo``
     - erasure coding only: defines the erasure coding algorithm to use.
   * - ``k``
     - erasure coding only: defines the number of data chunks.
   * - ``m``
     - erasure coding only: defines the number of parity chunks.

See also: `Erasure Coding`_.

.. _`Erasure Coding`: ./configuration_ec.html

Usage
-----

When an object is pushed, the storage policy is chosen in the following order:

- Object-level: when the Storage Policy is explicitly specified when pushing
- Container-level: when the container where the object is created specifies a Storage Policy to use
- Namespace-level: default behavior, uses the policy defined in /etc/oio/sds/[NS]/conscience-X/conscience-X.conf

See also: `OpenIO SDS Configuration`_.

.. _`OpenIO SDS Configuration`: ./configuration_namespace.html
