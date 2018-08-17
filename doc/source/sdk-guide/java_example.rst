.. _ref-sdk-java:

========
Java API
========

This sections describes how to install and use the `OpenIO Java API <../../oio-api-java-doc>`_

Install
-------

Download the latest version from the `Maven Repository`_.

.. _Maven Repository: https://mvnrepository.com/artifact/io.openio.sds/openio-api/0.7.1

Basic Concepts
--------------

An Object Storage API differs from a conventional filesystem: instead of directories and files, you manipulate containers where you store objects. A container can hold millions of objects.

There is no notion of hierarchy with containers: you cannot nest a container within an other, however you can emulate a nested folder structure with a naming convention for your objects. For example, with an object name such as "documents/work/2015/finance/report.pdf" you can retrieve your files using the appropriate "path" prefix.

In this SDK, to manipulate Containers and Objects, all you need to do is to initialize a ``Client`` object. To initialize it, you need the namespace name.
Endpoint URLs and all other configuration options will be loaded from ``/etc/oio/sds.conf.d/NAMESPACE`` (or ``~/.oio/sds.conf`` if you have deployed from source).

   .. code-block:: java

      Client client = ClientBuilder.newClient(NAMESPACE, PROXY_URL);

All of the sample code that follows assumes that you have correctly initialized a ``Client`` object.

Accounts
--------

Accounts are a convenient way to manage storage containers. Containers always belong to a specific Account.

You can list containers for a specified Account. Accounts are also a great way to track your storage usage (Total bytes used, Total number of objects, Total number of containers).

The API lets you set and retrieve your own metadata on accounts.

Creating a Container
--------------------

Start by creating a container:

   .. code-block:: java

      Client client = ClientBuilder.newClient("OPENIO", "http://127.0.0.1:6000");
      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER);
      ContainerInfo container = client.createContainer(url);
      System.out.println(container);

Note that if you try to create a container using the name of one that already exists, the request is ignored.

Showing the description of a Container
--------------------------------------

To show the description of a container:

   .. code-block:: java

      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER);
      Map<String,String> properties = client.getContainerProperties(url);
      System.out.println(properties);


Note that if you try to get a non-existent container, a ``ContainerNotFoundException`` exception is raised.

Storing Objects
---------------

This example creates an object named ``object.txt`` with the data provided, in the container ``CONTAINER``:

   .. code-block:: java

      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER, "object.txt");
      Client client = ClientBuilder.newClient("OPENIO", "http://127.0.0.1:6000");
      String myString = "Content example";
      InputStream data = new ByteArrayInputStream(myString.getBytes());
      long size = myString.length();
      ObjectInfo object = client.putObject(url, size, data);
      System.out.println(object);

Note that if you try to store an object in a non-existent container, a ``ContainerNotFoundException`` exception is raised.

Retrieving Objects
------------------

Note that if you try to retrieve a non-existent object, an ``ObjectNotFoundException`` exception is raised.

This sample code stores an object and retrieves it using the different parameters.

.. code-block:: java

      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER, "object.txt");
      ObjectInfo object = client.getObjectInfo(url);
      InputStream data = client.downloadObject(object);

Deleting Objects
----------------

Example:

.. code-block:: java

      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER, "object.txt");
      client.deleteObject(url);

Note that if you try to delete a non-existent object, an ``ObjectNotFoundException`` exception is raised.

Container and Object Metadata
-----------------------------

The Object Storage API lets you set and retrieve your own metadata on containers and objects.

.. code-block:: java

      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER);
      Map<String,String> properties = client.getContainerProperties(url);
      System.out.println(properties);

It should output an empty Map, unless you added metadata to this container.

.. code-block:: java

      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER);
      Map<String,String> properties = new HashMap<String,String>();
      properties.put("color", "blue");
      properties.put("flag", "true");
      client.setContainerProperties(url, properties);

      properties = client.getContainerProperties(url);
      System.out.println(properties);

It should now output:

.. code-block:: java

      {color=blue, flag=true}

This is very similar for objects. You can use the methods ``getObjectProperties()`` and ``setObjectProperties()``.

Listing Objects
---------------

.. code-block:: java

      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER);
      ListOptions options = new ListOptions();
      ObjectList objectList = client.listContainer(url, options);
      List<ObjectView> list = objectList.objects();
      System.out.println(list);

This returns a list of objects stored in the container.

Since containers can hold millions of objects, there are several methods to filter the results.

Filters:

- ``marker`` - Indicates where to start the listing from.
- ``prefix`` - If set, the listing only includes objects whose name begin with its value.
- ``delimiter`` - If set, excludes the objects whose names contain its value. delimiter only takes a single character.
- ``limit`` - Indicates the maximum number of objects to return in the listing.

To illustrate these features, you can create some objects in a container:

.. code-block:: java

      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER);
      client.createContainer(url);
      String myString = "sample";
      long size = myString.length();
      InputStream data;

      for (int i = 0; i < 5; i++) {
          data = new ByteArrayInputStream(myString.getBytes());
          url = OioUrl.url(ACCOUNT, CONTAINER, "object" + i);
          client.putObject(url, size, data);
      }

      for(char id = 'a'; id <= 'd'; id++) {
          data = new ByteArrayInputStream(myString.getBytes());
          url = OioUrl.url(ACCOUNT, CONTAINER, "foo/" + id);
          client.putObject(url, size, data);
      }

First list all the objects:

.. code-block:: java

      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER);
      ListOptions options = new ListOptions();
      ObjectList objectList = client.listContainer(url, options);
      List<ObjectView> list = objectList.objects();
      for (ObjectView object : list)
          System.out.println(object.name());

It should output:

.. code-block:: java

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

.. code-block:: java

      ListOptions options = new ListOptions();
      options.limit(4);
      options.marker("");
      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER);
      ObjectList objectList = client.listContainer(url, options);
      List<ObjectView> list = objectList.objects();
      List<String> names = new ArrayList<String>();
      for (ObjectView object : list)
          names.add(object.name());
      System.out.println("Objects: " + names);
      while (! list.isEmpty()) {
          options.marker(list.get(list.size() - 1).name());
          objectList = client.listContainer(url, options);
          list = objectList.objects();
          names = new ArrayList<String>();
          for (ObjectView object : list)
              names.add(object.name());
          System.out.println("Objects: " + names);
      }

Here is the result:

.. code-block:: java

      Objects: [foo/a, foo/b, foo/c, foo/d]
      Objects: [object0, object1, object2, object3]
      Objects: [object4]
      Objects: []

How to use the ``prefix`` parameter:

.. code-block:: java

      ListOptions options = new ListOptions();
      options.prefix("foo");
      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER);
      ObjectList objectList = client.listContainer(url, options);
      List<ObjectView> list = objectList.objects();
      List<String> names = new ArrayList<String>();
      for (ObjectView object : list)
          names.add(object.name());
      System.out.println("Objects: " + names);

This only outputs objects starting with "foo":

.. code-block:: java

      Objects: [foo/a, foo/b, foo/c, foo/d]

How to use the ``delimiter`` parameter:

.. code-block:: java

      ListOptions options = new ListOptions();
      options.delimiter("/");
      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER);
      ObjectList objectList = client.listContainer(url, options);
      List<ObjectView> list = objectList.objects();
      List<String> names = new ArrayList<String>();
      for (ObjectView object : list)
          names.add(object.name());
      System.out.println("Objects: " + names);

This excludes all the objects in the nested ``foo`` folder.

.. code-block:: java

      Objects: [object0, object1, object2, object3, object4]

Note that if you try to list a non-existent container, a ``ContainerNotFoundException`` exception is raised.

Deleting Containers
-------------------

There is several options to delete containers. Example:

.. code-block:: java

      OioUrl url = OioUrl.url(ACCOUNT, CONTAINER);
      client.deleteContainer(url);

You cannot delete a container if it still holds objects, if you try to do so a ``ContainerNotEmptyException`` exception is raised.

Note that if you try to delete a non-existent container, a ``ContainerNotFoundException`` exception is raised.
