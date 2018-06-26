=================
System management
=================

OpenIO SDS offers several tools for system management, for customers of any
size and with different needs. A comprehensive web UI us developed directly on
top of the OpenIO CLI and management APIs. That approach allows the customers
to build their own customised user interface and integrate commands in their
scripts to automate tasks.

Deployment tools
----------------
A complete set of pre-built scripts, designed for easily installing and
configuring marge-scale clusters, simplifies the deployment and configuration
activities in large scale deployments.

CLI / Command Line Interface
----------------------------
A central tool provides CLI comprehensive access to the Python native API, with
a consistent presentation of all the module. Easily extended, it is easy to
use and simplifies the management of an OpenIO SDS cluster.

The CLI tools mostly requires a network accesses to the grid, meaning the
tools is meant to be run on grid nodes or their clients.

.. code-block:: text

   openio action ${container_id}/${objectid}

WebUI
-----
Graphical User Interface that offers an overview of cluster status and
enables easy monitoring for day-to-day operations without using the CLI. A
comprehensive dashboard to get the status of the cluster in real time
which also allow to perform most day-to-day task including user management,
cluster expansion and maintenance as well as performance analysis.

Billing API
-----------
OpenIO’s customers can take advantage of this API to get relevant information
for any account configured in the system, its status and all the metrics that
can be used to compute the exact amount of resources consumed by the users.


