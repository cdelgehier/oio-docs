.. _ref-sdk-python:

==========
Python API
==========

This sections describes how to install and use the :doc:`OpenIO SDS Python API <python-api/modules>`.

Install
-------

Install the latest version directly from Github:

.. code-block:: shell

   pip install git+git://github.com/open-io/oio-sds.git@{{OIO_SDS_BRANCHNAME}}

Basic Concepts
--------------

An Object Storage API differs from a conventional filesystem: instead of directories and files, you manipulate containers where you store objects. A container can hold millions of objects.

There is no notion of hierarchy with containers: you cannot nest a container within another, however you can emulate a nested folder structure with a naming convention for your objects. For example, with an object name such as “documents/work/2015/finance/report.pdf” you can retrieve your files using the appropriate path prefix.

In this SDK, to manipulate Containers and Objects, all you need to do is to initialize an ``ObjectStorageApi`` object. To initialize it, you need the namespace name.
Endpoint URLs and all other configuration options will be loaded from ``/etc/oio/sds.conf.d/NAMESPACE`` (or ``~/.oio/sds.conf`` if you have deployed from source).

A minimal configuration file would be:

.. code-block:: text

   [NAMESPACE]
   proxy=http://YOUR_IP_ADRESS:6006


Where NAMESPACE is the name of your namespace.

.. code-block:: python

   from oio import ObjectStorageApi
   s = ObjectStorageApi(NAMESPACE)

All of the sample code that follows assumes that you have correctly initialized an ``ObjectStorageApi`` object.

Accounts
--------

Accounts are a convenient way to manage storage containers. Containers always belong to a specific Account.

You can list containers for a specified Account. Accounts are also a great way to track your storage usage (Total bytes used, Total number of objects, Total number of containers).

The API lets you set and retrieve your own metadata on accounts.

To access the accounts service, you'll need to use the `oio.account.client.AccountClient` class.

.. code-block:: python

   from oio.account.client import AccountClient
   ac = AccountClient({"namespace": "NAMESPACE"}, proxy_endpoint="http://YOUR_IP_ADDRESS:6006")

   # Account creation: Returns true if everything went well.
   ac.account_create("m_account_name")


Note that the `proxy_endpoint` parameter is optional if you have the configuration file. This keyword was added in version 4.0.0 of OpenIO SDS.


Creating a Container
--------------------

Start by creating a container:

.. code-block:: python

   s.container_create(ACCOUNT, CONTAINER)

Note that if you try to create a container using the name of one that already exists, the request is ignored.

Showing the description of a Container
--------------------------------------

To show the description of a container:

.. code-block:: python

   print s.container_get_properties(ACCOUNT, CONTAINER)


Note that if you try to get a non-existent container, a ``NoSuchContainer`` exception is raised.

Storing Objects
---------------

This example creates an object named ``object.txt`` with the data provided, in the container ``CONTAINER``:

.. code-block:: python

   data = "Content example"
   s.object_create(ACCOUNT, CONTAINER, obj_name="object.txt", data=data)

Note that if you try to store an object in a non-existent container, a ``NoSuchContainer`` exception is raised.

Retrieving Objects
------------------

The methods returns a generator; you must iterate on the generator to retrieve the content.

Note that if you try to retrieve a non-existent object, a ``NoSuchObject`` exception is raised.

This sample code stores an object and retrieves it using the different parameters.

.. code-block:: python

   print "Fetch object"
   meta, stream = s.object_fetch(ACCOUNT, CONTAINER, "object.txt")
   print "".join(stream)

Deleting Objects
----------------

Example:

.. code-block:: python

   s.object_delete(ACCOUNT, CONTAINER, "object.txt")

Note that if you try to delete a non-existent object, a ``NoSuchObject`` exception is raised.

Container and Object Metadata
-----------------------------

The Object Storage API lets you set and retrieve your own metadata on containers and objects.

.. code-block:: python

      meta = s.container_get_properties(ACCOUNT, CONTAINER)
      print "Metadata:", meta['properties']

It should output an empty dict, unless you have added metadata to this container.
The method returns a dictionary with two keys, ``properties`` and ``system``, which contain
respectively user set properties and system properties.

.. code-block:: python

      new_meta = {"color": "blue", "flag": "true"}
      s.container_set_properties(ACCOUNT, CONTAINER, properties=new_meta)

      meta = s.container_get_properties(ACCOUNT, CONTAINER)
      print "Metadata:", meta['properties']

It should now output:

.. code-block:: python

      Metadata: {u'color': u'blue', u'flag': u'true'}

This is very similar for objects. You can use the methods ``object_get_properties()``
(``object_show()`` in early versions) and ``object_set_properties()``.

Listing Objects
---------------

.. code-block:: python

      print s.object_list(ACCOUNT, CONTAINER)

This returns a list of objects stored in the container.

Since containers can hold millions of objects, there are several methods to filter the results.

Filters:

- ``marker`` - Indicates where to start the listing from.
- ``end_marker`` - Indicates where to end the listing.
- ``prefix`` - If set, the listing only includes objects whose name begin with its value.
- ``delimiter`` - If set, excludes the objects whose names contain its value. delimiter only takes a single character.
- ``limit`` - Indicates the maximum number of objects to return in the listing.

To illustrate these features, you can create some objects in a container:

.. code-block:: python

      s.container_create(ACCOUNT, CONTAINER)

      for id in range(5):
          s.object_create(ACCOUNT, CONTAINER, obj_name="object%s" % id, data="sample")

      start = ord("a")
      for id in xrange(start, start + 4):
          s.object_create(ACCOUNT, CONTAINER, obj_name="foo/%s" % chr(id), data="sample")

First list all the objects:

.. code-block:: python

      l = s.object_list(ACCOUNT, CONTAINER)
      objs = l['objects']

      for obj in objs:
          print obj['name']

It should output:

.. code-block:: python

      foo/a
      foo/b
      foo/c
      foo/d
      object0
      object1
      object2
      object3
      object4

Then use the paginating features:

.. code-block:: python

      limit = 4
      marker = ""
      l = s.object_list(ACCOUNT, CONTAINER, limit=limit, marker=marker)
      objs = l['objects']
      print "Objects:", [obj['name'] for obj in objs]
      while objs:
          marker = objs[-1]['name']
          l = s.object_list(ACCOUNT, CONTAINER, limit=limit, marker=marker)
          objs = l['objects']
          print "Objects:" , [obj['name'] for obj in objs]

Here is the result:

.. code-block:: python

      Objects: ['foo/a', 'foo/b', 'foo/c', 'foo/d']
      Objects: ['object0', 'object1', 'object2', 'object3']
      Objects: ['object4']
      Objects: []

How to use the ``prefix`` parameter:

.. code-block:: python

      l = s.object_list(ACCOUNT, CONTAINER, prefix="foo")
      objs = l['objects']
      print "Objects:", [obj['name'] for obj in objs]

This only outputs objects starting with "foo":

.. code-block:: python

      Objects: ['foo/a', 'foo/b', 'foo/c', 'foo/d']

How to use the ``delimiter`` parameter:

.. code-block:: python

      l = s.object_list(ACCOUNT, CONTAINER, delimiter="/")
      objs = l['objects']
      print "Objects:", [obj['name'] for obj in objs]

This excludes all the objects in the nested ``foo`` folder.

.. code-block:: python

      Objects: ['object0', 'object1', 'object2', 'object3', 'object4']

Note that if you try to list a non-existent container, a ``NoSuchContainer`` exception is raised.

Deleting Containers
-------------------

There are several options to delete containers. Example:

.. code-block:: python

      s.container_delete(ACCOUNT, CONTAINER)

You cannot delete a container if it still holds objects, if you try to do so a ``ContainerNotEmpty`` exception is raised.

Note that if you try to delete a non-existent container, a ``NoSuchContainer`` exception is raised.
