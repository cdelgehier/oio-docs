==============
Swift/S3 Proxy
==============

About the Swift/S3 proxy
~~~~~~~~~~~~~~~~~~~~~~~~

OpenIO SDS can be accessed with any application using the Amazon S3 API or the OpenStack Swift API.
To enable this, OpenIO provides a Swift/S3 proxy (project `oio-swift`).

The `oio-swift` project relies on the `OpenStack Swift <https://docs.openstack.org/swift/pike/getting_started.html>`_ proxy that is modified to integrate directly with OpenIO SDS.

Section DEFAULT
~~~~~~~~~~~~~~~

bind_ip
-------

IP address for the server to bind to.
The server must be mounted on a local interface.

* Format: dot-decimal representation of an IPv4 address or a colon-hexadecimal representation of an IPv6 address
* Default: `0.0.0.0`

.. code-block:: ini
   :caption: example

   bind_ip = 0.0.0.0


bind_port
---------

Port for the server to bind to.

* Format: positive integer less than 65535
* Default: 8080

.. code-block:: ini
   :caption: example

   bind_port = 8080

bind_timeout
------------

Time in seconds to attempt server bind before timeout.

* Format: positive integer
* Default: 30

.. code-block:: ini
   :caption: example

   bind_timeout = 30

backlog
-------

Maximum number of allowed pending TCP connections.

* Format: positive integer
* Default: 4096

.. code-block:: ini
   :caption: example

   bind_port = 4096

workers
-------

Describes the number of child processes. These child workers manage incoming
requests while the master process monitors its worker children.
When a child dies, it is spawned again.

* Format: positive integer
* Default: 1

.. code-block:: ini
   :caption: example

   workers = 4


max_clients
-----------

Maximum number of clients a single worker can process simultaneously.

* Format: positive integer
* Default: 1024

.. code-block:: ini
   :caption: example

   max_clients = 1024



user
----

User to run the server as.
If oio-swift is started as **root**, you can specify a user name or uid
to `setuid()`.

* Format: a declared user name or uid
* Default: None

.. code-block:: ini
   :caption: example

   user = openio


log_facility
------------

**syslog** log facility to use for both the access log and the error log.
Please refer to the syslog man page for more information.

* Format: a valid syslog facility name.
* Default: **LOG_LOCAL0**

.. code-block:: ini
   :caption: example

   log_facility = LOG_LOCAL0


log_address
-----------

Location where syslog sends logs to (both access and error).

* Format: a TCP/IP address or the path to a AF_LOCAL socket
* Default: **/dev/log**

.. TODO AF_LOCAL .. . SOCK_STREAM or SOCK_DGRAM (connected or not) ?

.. code-block:: ini
   :caption: example

   log_address = /dev/log


log_name
--------

Label used for logging.
This label is part of the syslog protocol and is present on each line.

* Format: a printable string with space
* Default: None

.. code-block:: ini
   :caption: example

   log_name = OIO,OPENIO,oioswift,1


eventlet_debug
--------------

If `true`, turn on debug logging for the python library `eventlet`.

* Format: boolean
* Default: false

.. code-block:: ini
   :caption: example

   eventlet_debug = false


sds_namespace
-------------

OpenIO SDS namespace to use.

.. code-block:: ini
   :caption: example

   sds_namespace = OPENIO


sds_proxy_url
-------------

OpenIO SDS `oio-proxy` URL to connect to cluster.

.. code-block:: ini
   :caption: example

   sds_proxy_url = http://127.0.0.1:6000


sds_default_account
-------------------

Default account name to use in OpenIO SDS.

.. code-block:: ini
   :caption: example

   sds_default_account = ACCT


sds_connection_timeout
----------------------

.. code-block:: ini
   :caption: example

   sds_connection_timeout = 5


sds_read_timeout
----------------

.. code-block:: ini
   :caption: example

   sds_read_timeout = 35


sds_write_timeout
-----------------

.. code-block:: ini
   :caption: example

   sds_write_timeout = 35


sds_pool_connections
--------------------

.. code-block:: ini
   :caption: example

   sds_pool_connections = 500


sds_pool_maxsize
----------------

.. code-block:: ini
   :caption: example

   sds_pool_maxsize = 500


sds_max_retries
---------------

.. code-block:: ini
   :caption: example

   sds_max_retries = 0


oio_storage_policies
--------------------

.. code-block:: ini
   :caption: example

   oio_storage_policies=SINGLE,THREECOPIES,EC


auto_storage_policies
---------------------

.. code-block:: ini
   :caption: example

   auto_storage_policies=EC,THREECOPIES:1,EC:262144


Section [pipeline:main]
~~~~~~~~~~~~~~~~~~~~~~~

The pipeline defines which middleware to use, and their invocation order.

pipeline
--------

.. code-block:: ini
   :caption: example

   pipeline = catch_errors gatekeeper healthcheck proxy-logging cache tempurl ratelimit authtoken swift3 s3token copy container-quotas account-quotas slo dlo versioned_writes proxy-logging proxy-server


Section [app:proxy-server]
~~~~~~~~~~~~~~~~~~~~~~~~~~

allow_account_management
------------------------

If `true`, allow PUT and DELETE on accounts.

* Format: boolean
* Default: false

.. code-block:: ini
   :caption: example

   allow_account_management = true


account_autocreate
------------------

If `true`, authorized accounts will be automatically created in OpenIO SDS.

* Format: boolean
* Default: false

.. code-block:: ini
   :caption: example

   account_autocreate = true

Section: [filter:catch_errors]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#catch_errors

Section: [filter:proxy-logging]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#proxy_logging

Section: [filter:tempurl]
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#tempurl

Section: [filter:authtoken]
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#authtoken
   paste.filter_factory = keystonemiddleware.auth_token:filter_factory
   auth_url =  http://127.0.0.1:35357
   auth_type = password
   project_domain_id = default
   user_domain_id = default
   project_name = service
   username = swift
   password = password

Section: [filter:keystoneauth]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#keystoneauth
   reseller_prefix = AUTH
   operator_roles = admin, swiftoperator
   reseller_admin_role = ResellerAdmin
   allow_overrides = true

Section: [filter:healthcheck]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#healthcheck
   disable_path =

Section: [filter:cache]
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#cache
   memcache_servers = 127.0.0.1:11211
   memcache_max_connections = 2

Section: [filter:ratelimit]
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#ratelimit

Section: [filter:copy]
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#copy
   object_post_as_copy = false

Section: [filter:dlo]
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#dlo

Section: [filter:slo]
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#slo
   max_manifest_segments = 1000
   max_manifest_size = 2097152

Section: [filter:container-quotas]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#container_quotas

Section: [filter:account-quotas]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#account_quotas

Section: [filter:gatekeeper]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:swift#gatekeeper

Section: [filter:hashedcontainer]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini
   :caption: example

   use = egg:oioswift#hashedcontainer

Sample configuration
~~~~~~~~~~~~~~~~~~~~

Here is a sample configuration:

.. code-block:: ini
   :caption: Complete example

   [DEFAULT]
   bind_port = 5999
   workers = 4
   user = openio
   log_facility = /dev/log
   log_level = INFO
   eventlet_debug = false

   sds_namespace = OPENIO
   sds_proxy_url = http://127.0.0.1:6000
   sds_default_account = ACCT

   sds_connection_timeout = 5
   sds_read_timeout = 35
   sds_write_timeout = 35

   sds_pool_connections = 500
   sds_pool_maxsize = 500
   sds_max_retries = 0

   oio_storage_policies=SINGLE,THREECOPIES,EC
   auto_storage_policies=EC,THREECOPIES:1,EC:262144

   [pipeline:main]
   # For keystone auth
   pipeline = catch_errors gatekeeper healthcheck proxy-logging cache tempurl ratelimit authtoken swift3 s3token copy container-quotas account-quotas slo dlo versioned_writes proxy-logging proxy-server
   # For tempauth
   # pipeline = catch_errors gatekeeper healthcheck proxy-logging cache tempurl ratelimit tempauth copy container-quotas account-quotas slo dlo versioned_writes proxy-logging proxy-server

   [app:proxy-server]
   use = egg:oioswift#main
   bind_ip = 0.0.0.0
   object_post_as_copy = false
   allow_account_management = true
   account_autocreate = true

   [filter:slo]
   use = egg:swift#slo

   [filter:dlo]
   use = egg:swift#dlo

   [filter:account-quotas]
   use = egg:swift#account_quotas

   [filter:container-quotas]
   use = egg:swift#container_quotas

   [filter:versioned_writes]
   use = egg:swift#versioned_writes
   allow_versioned_writes = true

   [filter:crossdomain]
   use = egg:swift#crossdomain

   [filter:gatekeeper]
   use = egg:swift#gatekeeper

   [filter:tempauth]
   use = egg:swift#tempauth
   user_test_tester=testing .admin

   [filter:proxy-logging]
   use = egg:swift#proxy_logging
   access_log_headers = false
   access_log_headers_only =

   [filter:authtoken]
   paste.filter_factory = keystonemiddleware.auth_token:filter_factory
   auth_url =  http://127.0.0.1:35357
   auth_type = password
   project_domain_id = default
   user_domain_id = default
   project_name = service
   username = swift
   password = password

   delay_auth_decision = True
   include_service_catalog = False
   memcached_servers = 127.0.0.1:11211

   [filter:s3token]
   use = egg:swift#s3token
   auth_uri = http://127.0.0.1:35357/v3
   reseller_prefix = AUTH_

   [filter:tempurl]
   use = egg:swift#tempurl

   [filter:catch_errors]
   use = egg:swift#catch_errors

   [filter:ratelimit]
   use = egg:swift#ratelimit

   [filter:healthcheck]
   use = egg:swift#healthcheck

   [filter:cache]
   use = egg:swift#memcache
   memcache_servers = 127.0.0.1:11211
   memcache_max_connections = 2

   [filter:copy]
   use = egg:swift#copy
   object_post_as_copy = false
