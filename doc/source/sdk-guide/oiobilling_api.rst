.. title:: Billing & Accounting RESTful API

==========================
OpenIO Billing service API
==========================

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

Check the service
~~~~~~~~~~~~~~~~~

List the configurations.

`GET /v1/info`

Output format
-------------

MIME type: `application/json`

+--------------------------------+---------+--------------------------+
| Key                            | Type    | Description              |
+================================+=========+==========================+
| oiobilling.version             | str     | `oiobilling` version     |
+--------------------------------+---------+--------------------------+
| sds_conf.proxy_url             | str     | Proxy URL                |
+--------------------------------+---------+--------------------------+
| sds_conf.namespace             | str     | Namespace                |
+--------------------------------+---------+--------------------------+
| prefixes.account_prefixes      | array   | Account prefixes         |
+--------------------------------+---------+--------------------------+
| prefixes.container_prefixes    | array   | Container prefixes       |
+--------------------------------+---------+--------------------------+

Example
-------

.. code-block:: http

      GET /v1/info HTTP/1.1
      Host: 127.0.0.1:5000
      User-Agent: curl/7.47.0
      Accept: */*

.. code-block:: http

      HTTP/1.1 200 OK
      Server: gunicorn/19.7.1
      Date: Thu, 10 Aug 2017 08:40:03 GMT
      Connection: keep-alive
      Content-Type: application/json
      Content-Length: 209

      {
          "prefixes":{
              "account_prefixes":[
                  "{account}-snapshot-"
              ],
              "container_prefixes":[
                  "{user}-snapshot-"
              ]
          },
          "oiobilling":{
              "version":"0.0.1"
          },
          "sds_conf":{
              "proxy_url":"http://127.0.0.1:6000",
              "namespace":"OPENIO"
          }
      }

Get the metrics
~~~~~~~~~~~~~~~

List the metrics.

`GET /v1/status`

Output format
-------------

MIME type: `application/json`

Example
-------

.. code-block:: http

      GET /v1/status HTTP/1.1
      Host: 127.0.0.1:5000
      User-Agent: curl/7.47.0
      Accept: */*

.. code-block:: http

      HTTP/1.1 200 OK
      Server: gunicorn/19.7.1
      Date: Fri, 11 Aug 2017 14:12:05 GMT
      Connection: keep-alive
      Content-Type: application/json
      Content-Length: 2

      {}

Fetch bill for a user
~~~~~~~~~~~~~~~~~~~~~

Return for a user:

- number of bytes
- number of objects
- incoming bandwidth (not implemented yet)
- outgoing bandwidth (not implemented yet)
- details of selected containers

`GET /v1/bill/fetch`

URL Parameters
--------------

+-------------+---------------+
| Parameter   | Description   |
+=============+===============+
| account     | Account ID    |
+-------------+---------------+
| user        | User ID       |
+-------------+---------------+

Output format
-------------

MIME type: `application/json`

+---------------------+---------+----------------------------------+
| Key                 | Type    | Description                      |
+=====================+=========+==================================+
| reference.account   | str     | Account ID                       |
+---------------------+---------+----------------------------------+
| reference.user      | str     | User ID                          |
+---------------------+---------+----------------------------------+
| storage.bytes       | int     | Numbers of bytes                 |
+---------------------+---------+----------------------------------+
| storage.objects     | int     | Number of objects                |
+---------------------+---------+----------------------------------+
| bandwidth.in        | int     | Incoming bandwidth               |
+---------------------+---------+----------------------------------+
| bandwidth.out       | int     | Outgoing bandwidth               |
+---------------------+---------+----------------------------------+
| items               | array   | Details of selected containers   |
+---------------------+---------+----------------------------------+

Example
-------

.. code-block:: http

      GET /v1/bill/fetch?account=myaccount&user=myuser HTTP/1.1
      Host: 127.0.0.1:5000
      User-Agent: curl/7.47.0
      Accept: */*

.. code-block:: http

      HTTP/1.1 200 OK
      Server: gunicorn/19.7.1
      Date: Thu, 10 Aug 2017 08:50:19 GMT
      Connection: keep-alive
      Content-Type: application/json
      Content-Length: 143

      {
          "items":[
          ],
          "bandwidth":{
              "out":0,
              "in":0
          },
          "storage":{
              "objects":0,
              "bytes":0
          },
          "reference":{
              "account":"myaccount",
              "user":"myuser"
          }
      }
