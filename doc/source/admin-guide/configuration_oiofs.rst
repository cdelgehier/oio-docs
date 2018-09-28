.. _label-oiofs-configuration:

====================
Filesystem Connector
====================

.. include:: ../business_oiofs.rst

Description
~~~~~~~~~~~

OpenIO provides a FUSE implementation to connect an OpenIO SDS namespace as
backend for a file system. Please refer to :ref:`label-oiofs-architecture`
for more information.

Prerequisites
~~~~~~~~~~~~~

In this guide we assume that you have an OpenIO SDS namespace that is ready to use,
in version **{{OIO_SDS_BRANCHNAME}}**, and an oio-fs connector in version
**{{OIO_FS_BRANCHNAME}}**.

Its name is **OPENIO** and it is accessible through an `oio-proxy` at
**127.0.0.1:6000**.

If you do not have such an installation, please refer to the :ref:`installation guide <ref-install-guide>`

In the subsequent sections, we will assume that the **${REDIS_ENDPOINT}** variable is
replaced with the actual network endpoint of the Redis service, e.g. the local
redis server at `127.0.0.1:6379`.


oio-fs configuration
~~~~~~~~~~~~~~~~~~~~

Prepare your system
^^^^^^^^^^^^^^^^^^^

If working with a regular non-privileged user, you will need to configure
FUSE permissions. In the file `/etc/fuse.conf`, you should uncomment the
line with `user_allow_other`.

If working in a container, be sure it has been started in privileged mode.
Please contact your system administrator if this is not the case, or to check
if it is.


Prepare oio-sds
^^^^^^^^^^^^^^^

To start working with an oio-fs mount point, you need to create the directory
reference that will gather all the container shards that hold the inodes of
your file system.

.. code-block:: console
   :caption: Init oio-sds for oio-fs usage

   $ mkfs.oiofs OPENIO/MyAccount/MyReference


This command will create a directory reference and associate several
properties to it. These properties are important, and they should not
change during the lifetime of the oio-fs volume.

.. code-block:: console
   :caption: Check the result

   $ openio --oio-ns OPENIO --oio-account MyAccount reference show MyReference
   +---------------------------------+-------------+
   | Field                           | Value       |
   +---------------------------------+-------------+
   | account                         | MyAccount   |
   | meta.oiofs_chunk_size           | 1048576     |
   | meta.oiofs_inodes_per_container | 65536       |
   | name                            | MyReference |
   +---------------------------------+-------------+


oiofs-fuse: CLI options
^^^^^^^^^^^^^^^^^^^^^^^

Many options are available for the `oiofs-fuse` command. Study these before using it:

.. code-block:: console
   :caption: oiofs-fuse help section

   # oiofs-fuse --help
   usage: oiofs-fuse [oio] mountpoint [options]

   general options:
     -o opt,[opt...]        mount options
     -h   --help            print help
     -V   --version         print version

   OIOFS options:
     -v   --verbose              be verbose
     --syslog-id <id>            set syslog id
     --oiofs-config              configuration file
     --oiofs-user-url <url>      set oiofs target user URL
     --cache-action <action>     action to perform if cache directory is not empty (recovery mode)
                                 'retrieve': retrieve the cache and continue like nothing happened
                                 'flush': retrieve and flush the cache and continue like nothing happened
                                 'erase': Remove all the files in the cache directory (Warning: the cache will be definitely erased)

   FUSE options:
     -d   -o debug          enable debug output (implies -f)
     -f                     foreground operation
     -s                     disable multi-threaded operation

     -o allow_other         allow access to other users
     -o allow_root          allow access to root
     -o auto_unmount        auto unmount on process termination
     -o nonempty            allow mounts over non-empty file/dir
     -o default_permissions enable permission checking by kernel
     -o fsname=NAME         set filesystem name
     -o subtype=NAME        set filesystem type
     -o large_read          issue large read requests (2.4 only)
     -o max_read=N          set maximum size of read requests

     -o max_write=N         set maximum size of write requests
     -o max_readahead=N     set maximum readahead
     -o max_background=N    set number of maximum background requests
     -o congestion_threshold=N  set kernel's congestion threshold
     -o async_read          perform reads asynchronously (default)
     -o sync_read           perform reads synchronously
     -o atomic_o_trunc      enable atomic open+truncate support
     -o big_writes          enable larger than 4kB writes
     -o no_remote_lock      disable remote file locking
     -o no_remote_flock     disable remote file locking (BSD)
     -o no_remote_posix_lock disable remove file locking (POSIX)
     -o [no_]splice_write   use splice to write to the fuse device
     -o [no_]splice_move    move data while splicing to the fuse device
     -o [no_]splice_read    use splice to read from the fuse device


The mandatory values are:

* `--oiofs-user-url` must match the oio-sds URL you used earlier, e.g.
  `OPENIO/MyAccount/MyReference`.
* `--oiofs-config` must point to a readable JSON file, whose keys are described
  below.

oiofs-fuse: configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`oio-fs` is configured with a JSON file, the possible keys (directives) are
described below.

.. contents::
   :local:

active_mode
-----------

Set to true to flush chunks to oio-sds.

* **OPTIONAL**
* Format: a boolean
* Default: **true**

attributes_timeout
------------------

Set the validity delay for the `oiofs` chunk attributes, in seconds.
Set to 0 to never cache these attributes.

* **OPTIONAL**
* Format: a positive integer
* Default: **0**


auto_retry
----------

By default, the cache doesn't retry on write/read/flush but returns EAGAIN.
This can cause some problems with local mounts. You can enable automatic
retry by setting `auto_retry` to `true`.

* **OPTIONAL**
* Format: **true** or **false**
* Default: **false**


cache_asynchronous
------------------

Configure cache management: set `cache_asynchronous` to `false` for
synchronous write-back behavior, or set `cache_asynchronous` to `true` to make
it asynchronous, thus relaxing security for better performance.

* **OPTIONAL**
* Format: **true** of **false**
* Default: **false**


cache_directory
---------------

Specify where oiofs-fuse will store its cached chunks of data.
It must point to a directory with `read` / `write` / `execute` permissions
granted to the user running `oiofs-fuse`.

No special options are required, but the operator is invited to dedicate a
directory on a partition that is as fast as possible. `tmpfs` caches show good results.

* **MANDATORY**
* Format: the path to an accessible directory
* Default: None


cache_size
----------

Sets how many bytes a cache can hold.

When the limit is reached, behavior is different depending on the type
of cache that has been configured. In cases of a synchronous cache (when
`cache_asynchronous` is set to `false`), content is expunged from the
cache until enough space is recovered for the file being accessed. In cases of
asynchronous caches, reaching the limit is a possible trigger for a write-back of
the cache.

* **MANDATORY**
* Format: a positive integer
* Default: None

cache_size_for_flush_activation
-------------------------------

To set the high-water mark. This is the size that will start a flush of the
cache when reached:

* **OPTIONAL**
* Format: a positive integer
* Default: 80% of `cache_size`

cache_size_on_flush
-------------------

On `cache reach flush activation` events, `oio-fs` will flush the cache until
its size reaches a value below the threshold set by `cache_size_on_flush`.

* **MANDATORY**
* Format: a positive integer
* Default: 50% of `cache_size`

cache_timeout
-------------

Set how many seconds pass between periodic flush of the cache.

* **OPTIONAL**
* Format: a positive integer
* Default: **5**

chunk_part_size
---------------
To set the size of a chunk part, this is only used when updating the
recovery cache:

* **OPTIONAL**
* Format: a positive integer
* Default: **1048576**

chunk_readahead
---------------

To set the chunk numbers to read ahead

* **OPTIONAL**
* Format: a positive integer
* Default: **0**

full_cache_timeout
------------------

On a full cache, if a request needs to retrieve a chunk, it will wait until
some space has been freed or it reaches a timeout defined by the following option:

* **OPTIONAL**
* Format: a positive integer
* Default: **0**

fuse_max_retries
----------------

The maximal number of rewrites (`auto_retry` must be set to `true`).

* **OPTIONAL**
* Format: a positive integer
* Default: **10**

ha_write_timeout
----------------

The write timeout of the distance cache (in milliseconds and > 0):

* **OPTIONAL**
* Format: a positive integer
* Default 500

http_server
------------

The address of the internal HTTP server that displays some metrics about the behavior
of the current oiofs-fuse. If no address is explicitly configured, no internal stats
server is started and no socket is exposed.

Please refer to this :ref:`section <ref-oiofs-sample-stat>` for an example output of
the internal HTTP server.

* **MANDATORY**
* Format: an ASCII string, the dot-decimal representation of an IPv4 address or a
  colon-hexadecimal representation of an IPv6 address, followed by a colon, then the TCP port.
* Default: None

ignore_flush
------------

When using an asynchronous cache, it is possible to postpone the `flush()`
command by setting `ignore_flush` to `true`.

* **OPTIONAL**
* Format: **true** or **false**
* Default: **false**


log_level
---------

Tune the verbosity of the `oio-fs` server. As a rule of thumb, verbosity levels
beyond **NOTICE** are suitable for production. Below that level, there is a risk
of flooding.

* **OPTIONAL**
* Format: a string among TRACE2, TRACE, DEBUG, INFO, NOTICE, WARN and ERROR.
* Default: **"NOTICE"**

max_flush_threads
-----------------

To improve overall performance, it is also necessary to avoid the connection to `oio-sds`
to prevent bottlenecks. `oio-fs` manages a pool of threads; these threads are created on demand until `max_flush_threads` is reached.
Any more demands will be blocked until a thread finishes its job (threads are reused).

* **OPTIONAL**
* Format: a positive integer
* Default: **10**

max_packed_chunks
-----------------

To increase speed, the cache aggregates chunks before sending them to `oio-sds`.
This is the maximum number of chunks per upload.

* **OPTIONAL**
* Format: a positive integer
* Default: **10**

max_redis_connections
---------------------

To improve overall performance it is necessary to avoid the connection to
Redis (Single or Sentinel) to prevent bottlenecks. `oio-fs` has been adapted to manage
a pool of connections; the connections are created on demand until `max_redis_connections`
is reached. Any attempt to get an outstanding connection is blocked until a connection
is released in the pool.

* **OPTIONAL**
* Format: a positive integer
* Default: **30**

recovery_cache_directory
------------------------

In High Availability setups, a second directory can be configured so that
`oio-fs` will also use it to locate its file chunks from the cache. It is up
to the operators to deploy that second partition with the suitable technology.

* **OPTIONAL**
* Format: an ASCII string, as a local path
* Default: None

redis_sentinel_name
-------------------

Set the name of the Redis service to use on the Redis Sentinel services, when
not using `redis_server`.

* **MANDATORY** (if not using `redis_server`)
* Format: an ASCII string
* Default: None


redis_sentinel_servers
----------------------

Set the locations of the Redis Sentinel services to target, when not using
`redis_server`.

* **MANDATORY** (if not using `redis_server`)
* Format: an array of ASCII strings representing valid network locations, i.e. dot-decimal representations of IPv4 addresses or a colon-hexadecimal representations of an IPv6 addresses, followed by a colon then the TCP port.
* Default: None


redis_server
------------

The network location of the Redis server that manages inodes persistence,
when not using a Redis Sentinel.

When targeting a Redis Sentinel (toward a replicated Redis cluster), you must
not use the `redis_server` configuration but rather use the couple
`redis_sentinel_server` and `redis_sentinel_name`.

* **MANDATORY** (if not using `redis_sentinel_server`)
* Format: dot-decimal representation of an IPv4 address or a colon-hexadecimal representation of an IPv6 address, followed by a colon the the TCP port.
* Default: None

sds_retry_delay
---------------

In some cases, oio-fs may be too fast for `oio-sds`, such as when there are a lot of `oio-fs`
instances on only one cluster. So, to not overload `oio-sds` with requests, you can set a time for it to wait after a failed request.

* **OPTIONAL**
* Format: a positive integer
* Default: **0**

sync_ha
-------

To only flush to the recovery_cache_directory on sync you need to change this value.

* **OPTIONAL**
* Format: a boolean
* Default: **true**


Additional notes
~~~~~~~~~~~~~~~~

Minimal setups
^^^^^^^^^^^^^^

The minimal file you need to provide must contain the 4 keys presented below:

.. code-block:: json
   :caption: Minimal configuration

   {
     "redis_server": "${REDIS_ENDPOINT}",
     "cache_directory": "/var/tmpfs/oiofs-cache",
     "cache_size": "5000000",
     "auto_retry": true
   }


Conservative setups
^^^^^^^^^^^^^^^^^^^

.. code-block:: json
   :caption: Conservative configuration

   {
     "redis_server": "${REDIS_ENDPOINT}",
     "cache_asynchronous": false,
     "cache_directory": "/var/tmpfs/oiofs-cache",
     "cache_size": 1073741824,
     "cache_size_on_flush": 536870912,
     "http_server": "127.0.0.1:8081",
     "log_level": "NOTICE",
     "auto_retry": true,
     "retry_delay": 500,
     "cache_timeout": 5,
     "max_packed_chunks": 10,
     "attributes_timeout": 0
   }


.. _ref-oiofs-sample-stat:

Sample stats
^^^^^^^^^^^^

Here is a sample of a request/response exchange between an HTTP client and the
stats server internal to the oiofs server. Output has been formatted here for
readability, but that won’t necessary be the case in actual production
deployments.

.. code-block:: http

   GET /stats HTTP/1.0
   Content-Length: 0


.. code-block:: http

   HTTP/1.0 200 OK
   Content-Type: application/json
   Content-Length: 3211

   {
       "cache_chunk_avg_age_microseconds": 45182744.85526317,
       "cache_chunk_count": 76,
       "cache_chunk_total_byte": 1073741824,
       "cache_chunk_used_byte": 638156800,
       "cache_read_avg_ms": 254.05700590625,
       "cache_read_count": 64,
       "cache_read_hit": 63,
       "cache_read_max_ms": 16256.968105,
       "cache_read_miss": 1,
       "cache_read_total_byte": 8388608,
       "cache_read_total_ms": 16259648378,
       "fuse_create_avg_ms": 0.564568625,
       "fuse_create_count": 128,
       "fuse_create_max_ms": 5.605509,
       "fuse_create_total_ms": 72264784,
       "fuse_flush_avg_ms": 0.0026561472868217055,
       "fuse_flush_count": 129,
       "fuse_flush_max_ms": 0.016336,
       "fuse_flush_total_ms": 342643,
       "fuse_forget_avg_ms": 10.371277872727273,
       "fuse_forget_count": 55,
       "fuse_forget_max_ms": 25.606962,
       "fuse_forget_total_ms": 570420283,
       "fuse_fsync_avg_ms": 0.002647375,
       "fuse_fsync_count": 128,
       "fuse_fsync_max_ms": 0.009823,
       "fuse_fsync_total_ms": 338864,
       "fuse_getattr_avg_ms": 0.00864849011299435,
       "fuse_getattr_count": 708,
       "fuse_getattr_max_ms": 0.996713,
       "fuse_getattr_total_ms": 6123131,
       "fuse_getxattr_avg_ms": 0.15538891055297852,
       "fuse_getxattr_count": 65536,
       "fuse_getxattr_max_ms": 4.525084,
       "fuse_getxattr_total_ms": 10183567642,
       "fuse_lookup_avg_ms": 0.1955374585492228,
       "fuse_lookup_count": 386,
       "fuse_lookup_max_ms": 1.915471,
       "fuse_lookup_total_ms": 75477459,
       "fuse_open_avg_ms": 0.013,
       "fuse_open_count": 2,
       "fuse_open_max_ms": 0.016417,
       "fuse_open_total_ms": 26000,
       "fuse_opendir_avg_ms": 0.027907,
       "fuse_opendir_count": 1,
       "fuse_opendir_max_ms": 0.027907,
       "fuse_opendir_total_ms": 27907,
       "fuse_read_avg_ms": 246.4167555151515,
       "fuse_read_count": 66,
       "fuse_read_max_ms": 16257.488012,
       "fuse_read_total_byte": 8650752,
       "fuse_read_total_ms": 16263505864,
       "fuse_readdir_avg_ms": 0.8259346666666666,
       "fuse_readdir_count": 3,
       "fuse_readdir_max_ms": 1.828243,
       "fuse_readdir_total_ms": 2477804,
       "fuse_release_avg_ms": 0.0027184186046511627,
       "fuse_release_count": 129,
       "fuse_release_max_ms": 0.015133,
       "fuse_release_total_ms": 350676,
       "fuse_releasedir_avg_ms": 0.013553,
       "fuse_releasedir_count": 1,
       "fuse_releasedir_max_ms": 0.013553,
       "fuse_releasedir_total_ms": 13553,
       "fuse_unlink_avg_ms": 1.3638342181818182,
       "fuse_unlink_count": 55,
       "fuse_unlink_max_ms": 5.007258,
       "fuse_unlink_total_ms": 75010882,
       "fuse_write_avg_ms": 0.02686740651321411,
       "fuse_write_count": 262144,
       "fuse_write_max_ms": 1815.726145,
       "fuse_write_total_byte": 1073741824,
       "fuse_write_total_ms": 7043129413,
       "sds_download_avg_ms": 90.156922,
       "sds_download_count": 1,
       "sds_download_failed": 0,
       "sds_download_max_ms": 90.156922,
       "sds_download_succeeded": 1,
       "sds_download_total_byte": 8388608,
       "sds_download_total_ms": 90156922,
       "sds_upload_avg_ms": 1023.9186892755681,
       "sds_upload_count": 352,
       "sds_upload_failed": 296,
       "sds_upload_max_ms": 11277.834337,
       "sds_upload_succeeded": 56,
       "sds_upload_total_byte": 2952790016,
       "sds_upload_total_ms": 360419378625
   }

Sample configuration from the http server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can retrieve the running configuration from the http server using the '/conf' route.

.. code-block:: http

   GET /conf HTTP/1.0
   Content-Length: 0

.. code-block:: http

   HTTP/1.0 200 OK
   Content-Type: application/json
   Content-Length: 731

   {
       "active_mode": true,
       "attributes_timeout": 0,
       "auto_retry": true,
       "cache_asynchronous": true,
       "cache_directory": "/tmp/oiofs",
       "cache_size": 1073741824,
       "cache_size_for_flush_activation": 858993459,
       "cache_size_on_flush": 536870912,
       "cache_timeout": 5,
       "chunk_part_size": 1048576,
       "chunk_readahead": 5,
       "full_cache_timeout": 0,
       "fuse_max_retries": 10,
       "ha_write_timeout": 500,
       "http_server": "127.0.0.1:8081",
       "ignore_flush": false,
       "log_level": "NOTICE",
       "max_flush_threads": 10,
       "max_packed_chunks": 10,
       "max_redis_connections": 30,
       "recovery_cache_directory": "",
       "redis_sentinel_name": "",
       "redis_sentinel_servers": "",
       "redis_server": "127.0.0.1:6379",
       "retry_delay": 500,
       "sds_retry_delay": 100,
       "sync_ha": true
   }
