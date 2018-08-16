.. _ref-solution-key-characteristics:
===================
Key Characteristics
===================

.. contents::
   :depth: 1
   :local:

The OpenIO project is an open source cloud platform for all storage infrastructures of all sizes.
It is dedicated to data-centric applications, built around OpenIO SDS, a highly
flexible object store that  allows  users  to  build  infrastructures  that
can  respond  to  the  most  demanding  requirements,  both  in  terms  of
scalability  and  performance.

OpenIO SDS is a highly flexible solution that allows users to build storage
infrastructures that can respond to the most demanding requirements, both in
terms of scalability and performance. In this section, we briefly introduce
the most important characteristics of its design.

Innovative Scale-Out Design
---------------------------
OpenIO SDS is based on a grid of nodes, instead of a traditional cluster ring-like layout. It is flexible, resource conscious, and capable of supporting heterogeneous hardware. OpenIO SDS’s cluster organisation is is not based on static data allocation, usually associated with a *Chord* peer-to-peer distributed hash table algorithm, and common among object stores. Data and metadata hash tables are organized in a distributed directory, allowing the software to attain the same level of scalability but with better and more consistent performance, no matter the size of the cluster.

The initial installation of OpenIO can be very small and can grow in small increments. Scaling the cluster is easy and seamless: it is possible to add as many new nodes as needed at once, without affecting performance or data availability.

Users do not need to anticipate long-term capacity and performance: the system will be able to take advantage of new resources as soon as they are added to the cluster.

Hardware Agnostic
------------------
OpenIO SDS is a fully software-defined solution that runs on x86 and ARM with minimal
requirements (starting at 1 CPU core, 512 MB of RAM, 1 NIC, and 4 GB of
storage). It is supported in mixed physical and virtual environments as well as
deployed in containers, the cloud, or at the edge.

Cluster nodes can be different from each other, allowing different hardware
generations and capacities to be combined over time without affecting
performance and efficiency.

Conscience Technology - Dynamic Load Balancing
----------------------------------------------
Thanks to Conscience technology, each operation is always performed on the
most available node. Each node of the cluster computes a quality score every
few seconds and shares it on a distributed shared board accessible to all
nodes

Each time a new operation is requested, the best nodes are selected according
to customer’s fine-grained policies for optimal resource utilization, and for the
best performance.

Event-Driven
------------
OpenIO SDS catches all events that occur in the cluster and can pass them
up in the stack or directly to an application on a local node. OpenIO’s
Grid for Apps serverless framework takes advantage of all of OpenIO SDS's features
and can process all its events seamlessly: third-party solutions can also
be integrated. Grid for Apps is an application backend for micro
services, automated data processing workflows, and event-driven applications.

Multi-Tenancy
-------------
An OpenIO SDS cluster can have multiple logical domains as well as accounts and
containers. Data can be organized in different storage pools and protection
schemes. All these features are designed to segregate data and workloads
while keeping the system efficient.

No rebalancing
--------------
Conscience technology eliminates the need for cluster rebalancing.

When new nodes are added, they progressively offload nodes in place thanks to
the scoring mechanism. Their quality score is better than for older,
heavily-loaded nodes, and they are used more often. New resources are immediately
available ensuring that performance improves with the added resources.

With Conscience technology, OpenIO SDS is able to detect the efficiency
of each node deployed in the infrastructure and use it at its true capacity.
The load can be balanced on heterogeneous nodes, and Conscience will take
this into account to get the best performance from each node.
