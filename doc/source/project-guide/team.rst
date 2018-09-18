========
The team
========

Our Mission
-----------

OpenIO is an open source object storage solution introduced in 2015, though its
development started 10 years earlier. It is built on top of the groundbreaking
concept of Conscience, allowing dynamic behavior and human-free administration.

Have you ever wondered how to store multiple petabytes of data without being
overwhelmed by complex storage tasks and complicated application development?
Object storage is changing the way we look at enterprise-class storage, but
most existing solutions suffer lack of scalability. As storage needs increase
dramatically, and hardware evolves, users need to be able to adapt to these
changes and not play catch-up.

OpenIO’s Conscience technology makes scalable object storage simple: new
hardware is auto-discovered and can be used immediately without impacting
performance. Conscience is designed to leverage heterogenous hardware: it is
aware of the capabilities of each piece of hardware and distributes the load
accordingly. OpenIO solves your storage problem, from 1TB to Exabytes, for
now and for the future.

OpenIO’s technology has been proven at a massive scale, especially in email
storage, with 10+ petabytes managed.

Our story
---------

In the data center of the company we were working for in 2006, storage needs
were growing exponentially. Our traditional NAS/SAN storage solution was
overwhelming the team charged with running these platforms.

This led us to conceive of a scalable object storage solution. Since most of
the data we were dealing with was made up of immutable objects, it was possible
to switch to a web-like GET/PUT/DELETE paradigm instead of a POSIX filesystem
API. This approach would also make it possible to eliminate the complex hardware
required to run these filesystems in a fully distributed manner.

Some object storage solutions existed at the time but most of them were designed
for the sole purpose of storing a small number of huge files, addressing large
storage capacities with a relatively small amount of metadata. Most of these
solutions were based on a single metadata node, avoiding the complexity of a
distributed directory. Most of them were also made for non-production
environments, and were not resilient enough, since the metadata node was a
single point of failure (SPOF).

Our goal was to store huge numbers of relatively small files produced by end
users, such as email. This would eventually use a large storage capacity,
but needed to be accessed with the lowest possible latency. Also, maximum
availability was essential, since service level agreements were strict for
these critical end-user services.

In late 2006, we designed our own solution with a massively distributed
directory. It enabled a true scale-out design:

* Each node would contain a part of the directory, so that the I/O intensive
  metadata load would be distributed across the cluster
* Each new node would be immediately used, so there was no need to re-dispatch
  existing data to benefit from new hardware
* Data storage would be decoupled from metadata storage, providing true
  scalability and unmatched performance

The solution had also to be hardware agnostic and support heterogeneous
deployments. It needed to support hardware from multiple vendors, and  multiple
storage technologies, from simple single-drive x86 hosts to high-end NAS and SAN
arrays that would be re-used behind x86 servers.

We built the first production-ready version of this object storage solution
in 2008, and the first massive production of a large-scale email system started
the following year. Since then, the solution has been used to store 10+
petabytes of data, 10+ billions of objects, with 20 Gbps of bandwidth at peak
hours, and with low-latency SLAs enforced 24/7.

As the solution was designed as a general-purpose object storage solution, it
was soon used in multiple environments like email, consumer cloud storage,
video archiving, healthcare systems, voice call recordings, and more.

This object storage solution became open source in 2012.

Today, OpenIO’s mission is to support the open source community and to make
the solution widely available, especially for the most demanding use cases.
