===========
Data Access
===========

.. image:: ../../../images/openio-arch-access-gateway-scalability.png
   :width: 600 px

.. contents::
   :depth: 1
   :local:

S3 API
++++++
OpenIO SDS is compatible with the Amazon® S3 API. Amazon S3 is the most common
and *de facto* standard object storage API. With S3 you can manage
objects with or without versions, or buckets of objects. Using OpenIO SDS as a
backend for Amazon S3 clients, your infrastructure will take advantage of all
the gateways and applications already available on the market, on premises,
and with all the benefits coming from SDS, including features like the
read-after-write consistency that S3 lacks.

Please check the ":ref:`label-s3-compliancy`" of OpenIO SDS.

Openstack Swift API
+++++++++++++++++++
OpenIO SDS is compatible with the OpenStack® Object Storage REST API.
Application integration becomes easy with this standard REST protocol. This API
can take advantage of many features available in OpenIO SDS withoutmajor
tradeoffs.

OpenIO FS
+++++++++
If you need to work with legacy use cases and export an OpenIO SDS account as a file system, you can use OpenIO FS. Locally mounted, you can then export it with NFS or SMB / CIFS protocols. High-availability extensions can be added on top of these protocols for best-in-class integration with a legacy filesystem architecture, while providing all the benefits of the OpenIO suite.

Please refer to ":ref:`label-oiofs-architecture`" or ":ref:`label-oiofs-configuration`"
for more information.

Client SDKs
+++++++++++
With the benefit of gateways, clients are easy to write. They all make use of
the gateway layer and only have to efficiently manage data streams. Currently, 
**C**, **Python**, and **Java** implementations are available.

These clients are considered “low-level,” since they are also involved in data
placement and are close to the remote services. Technically, they require
access to the whole grid of nodes; they are a part of it. Another option is to
deploy a REST gateway to access data from the outside, such as our
implementation of Amazon® S3 or OpenStack® SWIFT.
