.. title:: Internal services of OpenIO SDS

========
Services
========

.. contents::
   :local:

Introduction
~~~~~~~~~~~~

OpenIO SDS is composed of multiple services, running on commodity hardware,
from power-efficient systems to high-performance servers. Services are designed
to run across multiple nodes and do not require any specific collocation.

Here is a view of the different services available:

.. image:: ../../../images/openio-arch-solution.jpg
   :width: 600 px

Front Stack
~~~~~~~~~~~


OpenIO Swift
------------

The OpenIO Swift service handles Swift/S3 user requests.

Key characteristics:

- Stateless
- CPU and network intensive

Openstack Keystone
------------------

User authentication and service discovery is done through Openstack Keystone which is accessed directly by the client when using the Swift API, whereas when using S3, Keystone does not need to be publicly exposed.

Key characteristics:

- Stateless
- CPU intensive


MySQL
-----

MySQL is used as a backend for Openstack Keystone.

Key characteristics:

- Stateful
- CPU and network intensive
- Recommended to be deployed as cluster (using MariaDB Galera cluster) on at least 3 different servers.



OpenIO SDS
~~~~~~~~~~

The OpenIO SDS core solution is divided into multiple simple and lightweight services, which can be easily distributed on different nodes:

- Conscience services
- Directory services
- Data services
- Event services
- Account services


Conscience Services
-------------------
Conscience services are composed of a conscience service and conscience-agent services.

**Conscience**

The conscience service has two main functions:

- Service Discovery: A service uses Conscience to discover what kind of services are available in the namespace and how to contact them.
- Load Balancing: Conscience performs load balancing using real time metrics that are collected from the storage nodes. A score between 0 and 100 is computed using a configurable formula and then used to make a weighted random selection.

Key characteristics:

- Stateless
- CPU and network intensive
- Must be deployed on at least 3 different servers

**Conscience-agent**

This service monitors local services on the machine and also manage service registration in Conscience.

Key characteristics:

- Stateless
- Must be deployed on each server

Directory Services
------------------
Directory services (all the Meta0, Meta1 and Meta2 services), are responsible for handling directory requests and storing metadata.
All the directory services are replicated.

**Meta0**

The Meta0 directory stores the meta1 address for each container.
Meta0 handles a very limited and static number of entries (65,536).
There is only one instance of Meta0 per namespace.

Key characteristics:

- Stateful
- Very limited and static entries
- CPU and network intensive
- Must be deployed on 3 different servers
- Recommended to be deployed on high performance storage like SSD or NVMe

**Meta1**

The Meta1 directory stores the Meta2 address for each container.
The Meta1 directory can manage several millions of containers.

Key characteristics:

- Stateful
- CPU and network intensive
- Must be deployed on at least 3 different servers
- Recommended to be deployed on high performance storage like SSD or NVMe

**Meta2**

The Meta2 directory stores the content list for each container, and the chunk address for each piece of content.

Key characteristics:

- Stateful
- CPU, I/O, and network intensive
- Must be deployed on at least 3 different servers
- Recommended to be deployed on high performance storage like SSD or NVMe


**Zookeeper**

This service is used to store the directory services election statuses.

Key characteristics:

- Stateful
- Needs a quite high amount of RAM

**Metadata-proxy**

The metadata-proxy service is an HTTP directory proxy used to request Conscience/Meta0/Meta1/Meta2 services through a simple HTTP REST API.

Key characteristics:

- Stateless
- CPU intensive

Data Services
-------------

Data services are responsible for storing and serving the data (like the rawx),
handling part of the metadata depending on it (like the rdir), and the oio-blob-indexer.

**Rawx**

The Rawx service is a share-nothing service responsible for storing chunks. The interface uses a subset of WebDAV commands augmented with custom headers.

Key characteristics:

- Stateful
- IO intensive
- Must be deployed on every disk of the cluster

**Rdir**

Rdir is a reverse directory that stores references of chunks in a Rawx. This service is useful for rebuilding a Rawx.

Each Rawx has an Rdir instance associated that is not hosted on the same server.

Key characteristics:

- Stateful
- IO intensive
- Must be deployed on every server of the cluster

**oio-blob-indexer**

oio-blob-indexer is a crawler that re-indexes chunks in the Rdir

Key characteristics:

- Stateless
- I/O intensive
- Must be deployed on every server of the cluster

**ECD**

ECD (Erasure Coding Daemon) is used to manage Erasure Coding through C and Java SDKs.

Key characteristics:

- Stateless
- CPU intensive
- Must be deployed on every server of the cluster

Event Services
--------------

Event services handle asynchronous jobs. They are composed of the event-agent, which relies on a beanstalkd backend to manage jobs.

**Event-Agent**

Key characteristics:

- Stateless
- CPU intensive
- Must be deployed on every server of the cluster


**Beanstalk**

Key characteristics:

- Stateful
- I/O intensive
- Recommended to be deployed on high performance storage like SSD or NVMe


Account management
------------------

**Account**

The account service stores account related information such as the container list,
the number of objects, and the number of bytes occupied by all objects in the cluster.
Following an operation on a container (PUT, DELETE), events are created and consume
by the account service in order to update account information asynchronously.

Key characteristics:

- Stateful
- CPU intensive

**REDIS**

Redis is used by the account service to store account information.

Key characteristics:

- Stateful
- I/O intensive
- Recommended to be deployed on high performance storage like SSD or NVMe


Other Services
~~~~~~~~~~~~~~

Replicator
----------
The replicator service is a work queue consumer process. Its main purpose is to asynchronously replicate objects and containers from one local namespace to another geographically distant namespace.

Key characteristics:

- Stateless


Billing
-------
OIO-Billing is an HTTP service that retrieves the following information for an account, useful for billing:

- Number of bytes
- Number of objects
- Incoming bandwidth
- Outgoing bandwidth
- Details of selected containers

Key characteristics:

- Stateless

WebUI
-----
Graphical User Interface that offers an overview of cluster status and enables easy monitoring for day-to-day operations without using the CLI.
