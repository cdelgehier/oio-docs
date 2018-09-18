========================
Configure Erasure Coding
========================

Erasure coding uses a set of algorithms (similar to RAID 6) to allow the recovery
of missing data using a subset of the original data.
In theory, erasure coding uses less storage capacity than standard replication,
but offers the same guaranty of durability.
Erasure coding is transparent from the application perspective.

To use erasure coding, you must have a storage policy with an erasure coding data security policy configured.

Here is an example of a storage policy using erasure coding:

.. code-block:: text

   [STORAGE_POLICY]
   EC=NONE:EC_ISA_6_3

   [DATA_SECURITY]
   EC_ISA_6_3=ec/k=6,m=3,algo=isa_l_rs_vand,distance=1

This describes a storage policy named ``EC`` configured with a data security policy called ``EC_ISA_6_3`` that uses
the erasure coding backend ISA-L with the following parameters:

* ``algo``: code of the erasure coding backend.

* ``k``: number of data chunks.

* ``m``: number of parity chunks.

* ``distance``: distance between chunks.


.. list-table:: Erasure Code Backends
   :header-rows: 1
   :widths: 10 10 30

   * - Name
     - Code
     - Description
   * - ISA-L
     - ``isa_l_rs_vand``
     - Intel Storage Acceleration Library
   * - Liberasurecode
     - ``liberasurecode_rs_vand``
     - Software only EC Library that supports a Reed-Solomon backend.
   * - Jerasure
     - ``jerasure_rs_vand``
     - EC Library that supports Reed-Solomon backends.
   * - Jerasure (Cauchy)
     - ``jerasure_rs_cauchy``
     - EC Library that supports Cauchy backend.
   * - Flat XOR HD
     - ``flat_xor_hd``
     - Flat XOR backend.
   * - SHSS
     - ``shss``
     - NTT Lab hybrid EC backend.
