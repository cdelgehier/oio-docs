========
Overview
========

The OpenIO project is an open source cloud platform for all
sizes of platforms, which aims to be easy to use, install and connect
with your applications.

OpenIO provides a cloud platform built around storage for your applications,
for that it provides a set of interrelated services, each service offers a
dedicated API to facilitate integration.

The following table describes the OpenIO key caracteristics :

.. list-table:: OpenIO Key caracteristics
   :header-rows: 1
   :widths: 15 40

   * - Caracteristics
     - Description
   * - Multi-tenancy
     - Multi-tenancy is a core element of OpenIO SDS. Data is organized in two main levels: the account and the container. Data objects are stored sing the following hierarchy: namespace/account/container/object. Multiple namespaces can be configured in each cluster, providing multi-region/zone logical layouts for applications and segregated workloads depending on tenant or data geo-distribution needs. There is no classic subdirectory tree. Objects are stored in a flat structure at the container level. As with many other object storage solutions, it is possible to emulate a filesystem tree, but it has no physical reality.
   * - Hardware agnostic
     - Our technology is adaptive. OpenIO is able to detect the efficiency of each node deployed in the infrastructure and use it at its true capacity. The load can be balanced on heterogeneous nodes; OpenIO will take this into account to get the best performance from each node.
   * - No SPOF architecture
     - Every service used to serve data is redundant. From the top level of the directory to the chunk of data stored on disk, all information is duplicated. There is no SPOF (single point of failure): a node can be shut down, and it will not affect overall integrity or availability.
   * - Scale-out architecture
     - The minimal installation of OpenIO can be very small. It is even possible to start with a single instance Docker container in a VM for testing purposes. But to get full protection for the data, it is recommended to start with three servers/VMs. Scaling the cluster is easy and seamless; it is possible to add as many new nodes as needed at once, without affecting performance or data availability. Anticipating long-term capacity and performance  is not necessary; the system will be able to take advantage of new resources as soon as they are added to the cluster.
   * - Isolation
     - Each container is stored in a separate file (i.e. not in one unique data structure), and each chunk is also stored as a file. This greatly improves the overall robustness of the solution, and limits the impact of corruption or the loss of a single item.
   * - Integrity
     - Integrity checks are performed periodically to ensure that no silent data corruption or loss occurs.


The following table describes the OpenIO key features :

.. list-table:: OpenIO Key features
   :header-rows: 1
   :widths: 15 40

   * - Features
     - Description
   * - Tiering
     - With storage tiering, it is possible to configure classes of hardware, and select a specific one when needed to store data. This mechanism is called a storage policy. For example, a pool of high performance disks (like SSDs) can be configured in a special class to store objects that require low latency access. Several storage policies can be configured for the same namespace. They can be associated with specific hardware, but also with old or new objects, with a specific data protection mechanism for a particular dataset, etc.
   * - Replication and Erasure Coding
     - Configurable at each level of the architecture, directory replication secures namespace integrity. The service directory and metadata containers can be synchronously replicated to other nodes. Data can be protected and replicated in various manners, from simple replication that just creates multiple copies of data, to erasure coding, or even distributed erasure coding. This allows the user to choose the best compromise between data availability and durability, storage efficiency, and cost.
   * - Versioning
     - A container can keep several versions of an object. This is configured at the container-level, for all the objects at once. The setting is set at the container’s creation. It may be activated during the container’s life. If no value is specified, the namespace default value is considered. When versioning is disabled, pushing a new version of an object overrides the former version, and deleting an object marks it for removal. When versioning is enabled, pushing an object creates a new version of the object. Previous versions of an object can be listed and restored. The semantics of objects versioning has been designed to be compliant with both Amazon S3 and Swift APIs.
   * - Compression
     - Applied to chunks of data, this reduces overall storage cost. Decompression is made live during chunk download, with an acceptable extra latency and CPU usage. Compression is usually an asynchronous job to avoid hurting performance, and you can specify which data you want to compress (data ages, mime-types, users…).
   * - Geo-Redundancy
     - OpenIO SDS allows storage policies and data to be distributed across multiple datacenters. Depending on distance and latency requirements, data storage clusters can be stretched over multiple locations synchronously, or replicated to a different site asynchronously.
