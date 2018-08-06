.. _ref-solution-key-characteristics:
===================
Key characteristics
===================

.. contents::
   :depth: 1
   :local:

The OpenIO project is an open source cloud platform for all sizes of platforms,
dedicated to data-centric applications, built around OpenIO SDS, a highly
flexible object store that  allows  users  to  build  infrastructures  that
can  respond  to  the  most  demanding  requirements,  both  in  terms  of
scalability  and  performance.

OpenIO SDS is a highly flexible solution that allows users to build storage
infrastructures that can respond to the most demanding requirements, both in
terms of scalability and performance. In this section, we briefly introduce
the most important characteristics of its design.

Innovative Scale-out design
---------------------------
A grid of nodes, instead of traditional cluster ring-like layout, flexible,
resource conscious and capable of supporting heterogeneous hardware. OpenIO
SDS cluster organisation is is not based on static data allocation, which is
usually associated to *Chord* peer-to-peer distributed hash table algorithm,
pretty common among object stores. Data and metadata hash tables are organised
in a distributed directory, allowing to reach the same level of scalability
but with a better and more consistent performance, no matter the size of
the cluster.

The minimal installation of OpenIO can be very small and allows to grow with
small increments. Scaling the cluster is easy and seamless: it is possible to
add as many new nodes as needed at once, without affecting performance or
data availability.

Anticipating long-term capacity and performance is not necessary: the system
will be able to take advantage of new resources as soon as they are added to
the cluster.

Hardware agnostic
------------------
A fully software-defined solution that runs on x86 and ARM with minimal
requirements (starting at 1 CPU core, 512 MB of RAM, 1 NIC, and 4 GB of
storage). Supported in mixed physical and virtual environments as well as
deployed in containers, the cloud, or at the edge.

Cluster nodes can be different from each other, allowing different hardware
generations and capacities to be combined over time without affecting
performance and efficiency.

Conscience Technology - Dynamic load balancing
----------------------------------------------
Thanks to Conscience technology, each operation is always performed on the
most available node. Each node of the cluster computes a quality score every
few seconds and shares it on a distributed shared board accessible to all
nodes

Each time a new operation is requested, the best nodes are selected according
to customer’s fine-grained policies for optimal resource utilization, and
best performance.

Event-driven
------------
OpenIO SDS catches all events that occur in the cluster and can pass them
up in the stack or directly to an application on the local node. OpenIO’s
Grid for Apps serverless framework takes advantage of all OpenIO SDS features
and can process all its events seamlessly, and third-party solutions can
be integrated as well. Grid for Apps is an application backend for micro
services, automated data processing workflows, and event-driven applications.

Multi-tenancy
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
heavy-loaded nodes, and they’ll be used more often. New resources are immediately
available ensuring that performance improves with the added resources.

With Conscience Technology, OpenIO SDS is able to detect the efficiency
of each node deployed in the infrastructure and use it at its true capacity.
The load can be balanced on heterogeneous nodes, the Conscience will consider
this to get the best performance from each node.
