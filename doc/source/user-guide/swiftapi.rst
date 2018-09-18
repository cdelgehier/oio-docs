=================
Use the Swift API
=================

Setup
+++++

The simplest way to start using Swift over OpenIO is to follow these instructions
http://docs.openio.io/{{RELEASE}}/docker-image/ to run a standalone version of OpenIO SDS
with the Swift connector:

::

  $ docker run -ti --tty -p 127.0.0.1:6007:6007 openio/sds

You can use now the Swift API (described at https://developer.openstack.org/api-ref/object-store/).

Here are a few simple examples with the `curl` command.


Authentication
++++++++++++++

First, you have to retrieve your Authentication Token (`tempauth`):

::

  $ curl -i -H  "X-Auth-User: demo:demo" -H  "X-Auth-Key: DEMO_PASS"  http://127.0.0.1:6007/auth/v1.0/
  HTTP/1.1 200 OK
  X-Storage-Url: http://127.0.0.1:6007/v1/AUTH_demo
  X-Auth-Token-Expires: 86399
  X-Auth-Token: AUTH_tkdc3c3c9c09bb470ebd4561faf524244f
  Content-Type: text/html; charset=UTF-8
  X-Storage-Token: AUTH_tkdc3c3c9c09bb470ebd4561faf524244f
  Content-Length: 0
  X-Trans-Id: tx1ca2ca3465574968be754-005ae73afe
  X-Openstack-Request-Id: tx1ca2ca3465574968be754-005ae73afe
  Date: Mon, 30 Apr 2018 15:49:18 GMT

And expose it for the following examples:

::

  $ export STORAGE_URL=http://127.0.0.1:6007/v1/AUTH_demo
  $ export TOKEN=AUTH_tkdc3c3c9c09bb470ebd4561faf524244f


Create a New Container
++++++++++++++++++++++

::

  $ curl -i $STORAGE_URL/container3 -X PUT -H "X-Auth-Token:$TOKEN"
  curl -i $STORAGE_URL/container3 -X PUT -H "X-Auth-Token:$TOKEN"
  HTTP/1.1 201 Created
  Content-Type: text/html; charset=UTF-8
  Content-Length: 0
  X-Trans-Id: txe4da25b8234b4906b71e9-005ae73ca0
  X-Openstack-Request-Id: txe4da25b8234b4906b71e9-005ae73ca0
  Date: Mon, 30 Apr 2018 15:56:17 GMT


List Available Containers
+++++++++++++++++++++++++

::

  $ curl -i $STORAGE_URL'?format=json' -XGET -H "X-Auth-Token: $TOKEN"
  HTTP/1.1 200 OK
  Content-Length: 48
  X-Account-Object-Count: 0
  X-Timestamp: 1525103777.01753
  X-Account-Bytes-Used: 0
  X-Account-Container-Count: 1
  Content-Type: application/json; charset=utf-8
  X-Trans-Id: tx5b4997be98304abc9bbcf-005ae73ce5
  X-Openstack-Request-Id: tx5b4997be98304abc9bbcf-005ae73ce5
  Date: Mon, 30 Apr 2018 15:57:25 GMT

  [
      {
          "bytes": 0,
          "count": 0,
          "name": "container3"
      }
  ]


Upload New Content to a Container
+++++++++++++++++++++++++++++++++

::

  $ curl -XPUT -i -H "X-Auth-Token: $TOKEN" -T /etc/magic $STORAGE_URL/container3/test1/test2/test

  HTTP/1.1 100 Continue

  HTTP/1.1 201 Created
  Last-Modified: Mon, 30 Apr 2018 15:00:30 GMT
  Etag: "272913026300e7ae9b5e2d51f138e674"
  Content-Type: text/html; charset=UTF-8
  Content-Length: 0
  X-Trans-Id: tx5d6a44c25b6347349cce6-005ae72f8e
  X-Openstack-Request-Id: tx5d6a44c25b6347349cce6-005ae72f8e
  Date: Mon, 30 Apr 2018 15:00:30 GMT

List the Content of a Container
+++++++++++++++++++++++++++++++

::

  $ curl -i  $STORAGE_URL/container3?format=json  -X GET -H "X-Auth-Token:$TOKEN"
  HTTP/1.1 200 OK
  Content-Length: 179
  X-Container-Object-Count: 1
  Content-Type: application/json; charset=utf-8
  X-Timestamp: 1525099995.98386
  X-Container-Bytes-Used: 111
  X-Put-Timestamp: 1525099995.98386
  X-Trans-Id: txb0a53deed3704fecbdf58-005ae72f57
  X-Openstack-Request-Id: txb0a53deed3704fecbdf58-005ae72f57
  Date: Mon, 30 Apr 2018 14:59:35 GMT

  [
      {
          "bytes": 111,
          "content_type": "application/octet-stream",
          "hash": "272913026300e7ae9b5e2d51f138e674",
          "last_modified": "2018-04-30T14:59:09.000000",
          "name": "test1/test2/test"
      }
  ]


Delete an object
++++++++++++++++

::

  $ curl -XDELETE -i -H "X-Auth-Token: $TOKEN" $STORAGE_URL/container3/test1/test2/test
  HTTP/1.1 204 No Content
  Content-Type: text/html; charset=UTF-8
  Content-Length: 0
  X-Trans-Id: txd3efa8f6a63f45a194bf8-005ae72fc3
  X-Openstack-Request-Id: txd3efa8f6a63f45a194bf8-005ae72fc3
  Date: Mon, 30 Apr 2018 15:01:23 GMT

Delete a container
++++++++++++++++++

::

  $ curl -XDELETE -i -H "X-Auth-Token: $TOKEN" $STORAGE_URL/container3/test1/test2/test
  HTTP/1.1 204 No Content
  Content-Type: text/html; charset=UTF-8
  Content-Length: 0
  X-Trans-Id: txd3efa8f6a63f45a194bf8-005ae72fc3
  X-Openstack-Request-Id: txd3efa8f6a63f45a194bf8-005ae72fc3
  Date: Mon, 30 Apr 2018 15:01:23 GMT


Resources:

https://prosuncsedu.wordpress.com/2014/02/26/accessing-object-store-with-curl/
