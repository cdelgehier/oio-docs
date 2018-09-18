=================
System Management
=================

OpenIO SDS offers several tools for system management, for customers of any
size and with different needs. A comprehensive web UI was developed directly on
top of the OpenIO CLI and management APIs. This approach allows customers
to build their own customized user interface and integrate commands in their
scripts to automate tasks.

Deployment tools
----------------
A complete set of pre-built scripts, designed for easily installing and
configuring large-scale clusters, simplifies deployment and configuration
of large deployments.

CLI / Command Line Interface
----------------------------
A central tool provides comprehensive command-line access to the native Python
API, with a consistent presentation of all the modules. Easily extended,
it is easy to use and simplifies the management of an OpenIO SDS cluster.

The CLI tools mostly require network accesses to the grid, meaning the
tools are meant to be run on grid nodes or their clients.

.. code-block:: text

   openio action ${container_id}/${objectid}

WebUI
-----
This is a graphical user interface that offers an overview of cluster status
and enables easy monitoring for day-to-day operations without using the CLI. A
comprehensive dashboard allows users to see the status of the cluster in real
time, and to perform most day-to-day tasks including user management, cluster
expansion, and maintenance, as well as performance analysis.

Billing API
-----------
OpenIO’s customers can take advantage of this API to get relevant information
for any account configured in the system, its status, and all the metrics used
to compute the exact amount of resources consumed by users.
