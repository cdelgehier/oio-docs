=================================
Understand the format of the logs
=================================

The services in an OpenIO system respect a common format for their logs. Each
log item is a single line of text, encoded in UTF-8. A line is a sequence of
items separated by a sequence of white spaces. For an easy parsing, the variety
of the messages is organized around a recursion of envelopes (header and
payload). All the fields are always present on a line, and when a field is not
set it is represented by a single dash character.


.. contents::
   :local:

oio-swift
+++++++++

COMMON envelope
~~~~~~~~~~~~~~~

All the messages share this envelope. The first 3 fields depend on syslog,
and all the others are populated by the application.

.. list-table:: Common Header
   :widths: 20 100

   * - Timestamp
     - When the message has been issued. Should be displayed in ISO-8601
   * - Hostname
     - Where (on the platform) was the log trace emitted
   * - Instance ID
     - Logical identifier of the runninng application
   * - Loglevel
     - A value in the set: **error**, **warning**, **notice**, **info**, **debug**


ACCESS logs
~~~~~~~~~~~


.. list-table:: Fields from the SWIFT envelope
   :widths: 20 100

   * - Client IP
     - Swift’s guess at the end-client IP, taken from various headers in the request.
   * - Remote Address
     - The IP address of the other end of the TCP connection.
   * - Datetime
     - Timestamp of the request, in day/month/year/hour/minute/second format.
   * - Request Type
     - The HTTP verb in the request.
   * - Request Path
     - The path portion of the request.
   * - Protocol
     - The transport protocol used (currently one of http or https).
   * - Return Code
     - The response code for the request.
   * - Referer
     - The value of the HTTP Referer header.
   * - User Agent
     - The value of the HTTP User-Agent header.
   * - Auth Token
     - The value of the auth token. This may be truncated or otherwise obscured.
   * - Bytes Recvd
     - The number of bytes read from the client for this request.
   * - Bytes Sent
     - The number of bytes sent to the client in the body of the response. This is how many bytes were yielded to the WSGI server.
   * - Client Etag
     - The etag header value given by the client.
   * - Transaction ID
     - The transaction id of the request.
   * - Headers
     - The headers given in the request.
   * - Request Time
     - The duration of the request.
   * - Source
     - The “source” of the request. This may be set for requests that are generated in order to fulfill client requests, e.g. bulk uploads.
   * - Log Info
     - Various info that may be useful for diagnostics, e.g. the value of any x-delete-at header.
   * - Request Start Time
     - High-resolution timestamp from the start of the request.
   * - Request End Time
     - High-resolution timestamp from the end of the request.
   * - Policy Index
     - The value of the storage policy index.

In one log line, all of the above fields are space-separated and url-encoded. If any value is empty, it will be logged as a ``-``. This allows for simple parsing by splitting each line on whitespace.
New values may be placed at the end of the log line from time to time, but the order of the existing values will not change.

DEBUG logs
~~~~~~~~~~

.. list-table:: DEBUG header
   :widths: 20 100

   * - Payload
     - An arbitrary message.

Example
~~~~~~~

Below is an example of a single line of logs, as well as its mapping to the
compound parameters.

.. code-block:: text

    2018-05-17T09:30:19.429606+00:00 localhost OIO,OPENIO,oioswift,0: info  192.168.0.2 192.168.0.3 /May/2018/09/30/19 HEAD /test/ HTTP/1.0 200 - aws-sdk-java - - - - tx2a84a70d4be94ed9815e7-005afd4bab - 0.0060 - - 1526549419.422362089 1526549419.428388119 -


.. list-table:: Fields from the common envelope
   :widths: 20 100

   * - Timestamp
     - `2018-05-17T09:30:19.429606+00:00`
   * - Hostname
     - `localhost`
   * - Instance ID
     - `OIO,OPENIO,oioswift,0`
   * - Loglevel
     - `info`

.. list-table:: Fields from the ACCESS envelope
   :widths: 20 100


   * - Client IP
     - `192.168.0.2`
   * - Remote Address
     - `192.168.0.2`
   * - Datetime
     - `/May/2018/09/30/19`
   * - Request Type
     - `HEAD`
   * - Request Path
     - `/test/`
   * - Protocol
     - `HTTP/1.0`
   * - Return code
     - `200`
   * - Referer
     - `-`
   * - User Agent
     - `aws-sdk-java`
   * - Auth Token
     - `-`
   * - Bytes Recvd
     - `-`
   * - Bytes Sent
     - `-`
   * - Client Etag
     - `-`
  * - Transaction ID
    - `tx2a84a70d4be94ed9815e7-005afd4bab`
  * - Headers
    - `-`
  * - Request Time
    - `0.0060`
  * - Source
    - `-`
  * - Log Info
    - `-`
  * - Request Start Time
    - `1526549419.422362089`
  * - Request End Time
    - `1526549419.428388119`
  * - Policy Index
    - `-`

oio-sds: oio-proxy, oio-meta{0,1,2}-server
++++++++++++++++++++++++++++++++++++++++++



COMMON envelope
~~~~~~~~~~~~~~~

All the messages share this envelope. The first 3 fields depend on syslog,
and all the others are populated by the application.

.. list-table:: Common Header
   :widths: 20 100

   * - Timestamp
     - When the message has been issued. Should be displayed in ISO-8601
   * - Hostname
     - Where (on the platform) was the log trace emitted
   * - Instance ID
     - Logical identifier of the runninng application
   * - Process ID
     - Physical identifier of the currently running application
   * - Thread ID
     - Internal identifier of the control thread
   * - Domain
     - ``access``, ``log``, ``out``
   * - Payload
     - A data whose format will depend on the value of the ``Domain``
   * - Loglevel
     - A value in the set: **err**, **warning**, **notice**, **info**, **debug**


ACCESS logs
~~~~~~~~~~~

When a request has been managed, the service in charge will drop a single
line in its ACCESS log. All these lines have the same format: the common header
carries the ``access`` domain, and the payload is formatted as follows.

.. list-table:: ACCESS header
   :widths: 20 100

   * - Level
     - A value in the set: **ERR**, **WRN**, **NOT**, **INF**, **DBG**, **TR0**, **TR1**
   * - Local Address
     - The local network address the service is bound to
   * - Remote Address
     - The network address of the peer that connected to the service
   * - Request Type
     - The name of the request, a.k.a. the RPC method.
   * - Return Code
     - The numeric return code of the message.
   * - Request Time
     - How many microseconds it took to handle the request until a reply was ready (but not sent yet!)
   * - Request Size
     - How many bytes have been serialized for the reply. In case of HTTP requests, this doesn't include the headers.
   * - User ID
     - The ID of the end-user the request is issued for
   * - Session ID
     - The ID of the user's session, sometimes also named Request-Id, used for aggregation purposes.
   * - Payload
     - An arbitrary payload, often organized as a sequence of ``key=value`` pairs.


Let's mention the case of the ACCESS log for outgoing requests. It is triggered
by an option in the central configuration file, and the format of each line is
exactly the same as for incoming requests, with the exception of the ``Domain``
in the common envelope that is set to ``out``.


DEBUG logs
~~~~~~~~~~

Any service might also emit traces, generated by either a request or a
background task. The format is much less specified, dedicated for debugging
purposes, destined to be read by a human more than a parser.

.. list-table:: DEBUG header
   :widths: 20 100

   * - Level
     - A value in the set: **ERR**, **WRN**, **NOT**, **INF**, **DBG**, **TR0**, **TR1**
   * - Payload
     - An arbitrary message.


Example
~~~~~~~

Below is an example of a single line of logs, as well as its mapping to the
compound parameters.

.. code-block:: text

    2017-04-25T17:00:01.094517+02:00 localhost OIO,OPENIO,meta0,1: info 12159 1E9A access INF 127.0.0.1:6004 127.0.0.1:48780 M0_GET 200 89 91 - 742FBB9DC7674C7C7959957801F06B44 t=63 AAA0

The first 3 fields are set by syslog, making the ``Process ID`` field redundant.

.. list-table:: Fields from the common envelope
   :widths: 20 100

   * - Timestamp
     - `2017-04-25T17:00:01.094517+02:00`
   * - Hostname
     - `localhost`
   * - Instance ID
     - `OIO,OPENIO,meta0,1`
   * - Process ID
     - `12159`
   * - Thread ID
     - `1E9A`
   * - Domain
     - `access`
   * - Loglevel
     - `info`

The ``Domain`` is set to ``access``, so let's unpack the tail with the
appropriated format.

.. list-table:: Fields from the ACCESS envelope
   :widths: 20 100

   * - Level (ACCESS)
     - `INF`
   * - Local Address
     - `127.0.0.1:6004`
   * - Remote Address
     - `127.0.0.1:48780`
   * - Request Type
     - `M0_GET`
   * - Return Code
     - `200`
   * - Request Time
     - `89`
   * - Request Size
     - `91`
   * - User ID
     - `-`
   * - Session ID
     - `742FBB9DC7674C7C7959957801F06B44`
   * - Payload
     - `t=63 AAA0`

In this example, all the fields are always present as expected, but one
of the missing fields is defaulting to a dash. The final field is has an
arbitrary (or unspecified) format, it depends on the service
implementation.

The key ``t=`` represents the time (in microseconds) spent by a worker thread,
once the request has been polled out of the queue in front of the thread pool.
The difference between this time and the value of the ``Request Time`` field
of the ``access`` envelope is the delay spent in the queue. A large delay is
a sign of an heavily loaded service or, worse, a thread starvation.

Another key used by OpenIO SDS is ``e=``, that gives the root cause of the
error that occured. At the moment, there is no common format for that error,
but we tend to explain the error as a JSON object with ``status`` and a
``message`` field.

oio-sds: rawx services
++++++++++++++++++++++

COMMON envelope
~~~~~~~~~~~~~~~

All the messages share this envelope. The first 3 fields depend on syslog,
and all the others are populated by the application.

.. list-table:: Common Header
   :widths: 20 100

   * - Timestamp
     - When the message has been issued. Should be displayed in ISO-8601
   * - Hostname
     - Where (on the platform) was the log trace emitted
   * - Instance ID
     - Logical identifier of the runninng application
   * - Process ID
     - Physical identifier of the currently running application
   * - Thread ID
     - Internal identifier of the control thread
   * - Domain
     - ``access``, ``log``, ``out``
   * - Payload
     - A data whose format will depend on the value of the ``Domain``



ACCESS logs
~~~~~~~~~~~

When a request has been managed, the service in charge will drop a single
line in its ACCESS log. All these lines have the same format: the common header
carries the ``access`` domain, and the payload is formatted as follows.

.. list-table:: ACCESS header
   :widths: 20 100

   * - Level
     - A value in the set: **ERR**, **WRN**, **NOT**, **INF**, **DBG**, **TR0**, **TR1**
   * - Local Address
     - The local network address the service is bound to
   * - Remote Address
     - The network address of the peer that connected to the service
   * - Request Type
     - The name of the request, a.k.a. the RPC method.
   * - Return Code
     - The numeric return code of the message.
   * - Request Time
     - How many microseconds it took to handle the request until a reply was ready (but not sent yet!)
   * - Request Size
     - How many bytes have been serialized for the reply. In case of HTTP requests, this doesn't include the headers.
   * - User ID
     - The ID of the end-user the request is issued for
   * - Session ID
     - The ID of the user's session, sometimes also named Request-Id, used for aggregation purposes.
   * - Payload
     - An arbitrary payload, often organized as a sequence of ``key=value`` pairs.

Example
~~~~~~~

Below is an example of a single line of logs, as well as its mapping to the
compound parameters.

.. code-block:: text

   Apr 17 15:51:19 localhost.ec2.internal OIO,OPENIO,rawx,0 442 139668301539072 access INF 127.0.0.1:6004 127.0.0.1:38204 PUT 201 4697 4432 A05D07A89E3AD909B56346FE810B5CC6FAE8AD8339E4E3023A0DA4E41806780C 02469F5339E0D7D83AF59512967544C0 /EA8A1715C27ABA2A161CEB743D1BDC1A8B7AA277A4FF47F18857ED26F444B879

The first 3 fields are set by syslog, making the ``Process ID`` field redundant.

.. list-table:: Fields from the common envelope
   :widths: 20 100

   * - Timestamp
     - `Apr 17 15:51:19`
   * - Hostname
     - `localhost.ec2.internal`
   * - Instance ID
     - `OIO,OPENIO,rawx,0`
   * - Process ID
     - `442`
   * - Thread ID
     - `139668301539072`
   * - Domain
     - `access`


The ``Domain`` is set to ``access``, so let's unpack the tail with the
appropriated format.

.. list-table:: Fields from the ACCESS envelope
   :widths: 20 100

   * - Level (ACCESS)
     - `INF`
   * - Local Address
     - `127.0.0.1:6004`
   * - Remote Address
     - `127.0.0.1:38204`
   * - Request Type
     - `PUT`
   * - Return Code
     - `204`
   * - Request Time
     - `4697`
   * - Request Size
     - `4432`
   * - User ID
     - `A05D07A89E3AD909B56346FE810B5CC6FAE8AD8339E4E3023A0DA4E41806780C`
   * - Session ID
     - `02469F5339E0D7D83AF59512967544C0`
   * - Payload
     - `/EA8A1715C27ABA2A161CEB743D1BDC1A8B7AA277A4FF47F18857ED26F444B879`
