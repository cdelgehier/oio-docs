.. _label-oiobilling-configuration:

===================================
Configure an OpenIO Billing Service
===================================

.. include:: ../business_oiobilling.rst

.. contents::
   :local:

Description
~~~~~~~~~~~

OpenIO Billing is an HTTP service allowing to retrieve the following information for an account, useful for billing:

- number of bytes
- number of objects
- incoming bandwidth
- outgoing bandwidth
- details of selected containers

Sample configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

      [billing-server]
      bind_addr = 127.0.0.1
      bind_port = 5000
      workers = 2
      log_level = INFO
      log_facility = LOG_LOCAL0
      log_address = /dev/log
      syslog_prefix = OIO,OPENIO,billing,1

      # The namespace of your OpenIO-SDS installation
      sds_namespace = OPENIO
      # A specific URL to join the oio-proxy, your entry point to your OpenIO-SDS
      # namespace (optional)
      # sds_proxy_url = http://127.0.0.1:6000

      # The lists of prefixes
      account_prefixes =
          {account}-snapshot-
      container_prefixes =
          {user}-snapshot-

`sds_namespace`
  The SDS Namespace to serve. Example: `OPENIO`
`sds_proxy_url` (optional)
  The URL of the SDS proxy. Example: `http://127.0.0.1:6000`
`account_prefixes`
  The account prefixes to search. Example: `{account}-snapshot-`
`container_prefixes`
  The container prefixes to search. Example: `{user}-snapshot-`

Run
~~~

.. code-block:: shell

      oio-billing-server <conf>


Usage
~~~~~

See :ref:`label-oiobilling-api`.
