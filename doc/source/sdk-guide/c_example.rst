.. _ref-sdk-c:

=====
C API
=====

This sections describes how to install and use the `OpenIO SDS C SDK <../../oio-api-c-doc>`_

Install
-------

Download the latest version directly from GitHub:

   .. code-block:: shell

      git clone git://github.com/open-io/oio-sds.git

Basic Concepts
--------------

An Object Storage API differs from a conventional filesystem: instead of directories and files, you manipulate containers where you store objects. A container can hold millions of objects.

There is no notion of hierarchy with containers: you cannot nest a container within an other, however you can emulate a nested folder structure with a naming convention for your objects. For example with an object name such as "documents/work/2015/finance/report.pdf" you can retrieve your files using the appropriate "path" prefix.

In this SDK, you manipulate Containers and Objects, all you need to do is to initialize an ``oio_sds_s`` structure. To initialize it, you need the namespace name.
Endpoint URLs and all other configuration options will be loaded from ``/etc/oio/sds.conf.d/NAMESPACE`` (or ``~/.oio/sds.conf`` if you have deployed from source).

   .. code-block:: c

      struct oio_sds_s *client = NULL;
      struct oio_error_s *err = NULL;
      err = oio_sds_init(&client, NAMESPACE);
      g_assert_no_error((GError*)err);

All the sample code that follows assumes that you have correctly initialized an ``oio_sds_s`` structure.

Accounts
--------

Accounts are a convenient way to manage storage containers. Containers always belong to a specific Account.

You can list containers for a specified Account. Accounts are also a great way to track your storage usage (Total bytes used, Total number of objects, Total number of containers).

The API lets you set and retrieve your own metadata on accounts.

Creating a Container
--------------------

Start by creating a container:

   .. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);

      err = oio_sds_create(client, url);
      oio_url_clean(url);
      g_assert_no_error((GError*)err);

Note that if you try to create a container using the name of one that already exists, the request is ignored.

Showing the description of a Container
--------------------------------------

To show the description of a container:

   .. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);

      void _print_element (void *ctx, const char *key, const char *value) {
          (void) ctx;
          g_print("\"%s\": \"%s\", ", key, value);
      }

      err = oio_sds_get_container_properties(client, url, print_element, NULL);
      oio_url_clean(url);
      g_assert_no_error((GError*)err);


Note that if you try to get a non-existent container, an ``oio_error_s`` is returned.

Storing Objects
---------------

This example creates an object named ``object.txt`` with the data provided, in the container ``CONTAINER``:

   .. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);
      oio_url_set(url, OIOURL_PATH, "object.txt");

      struct oio_sds_ul_dst_s ul_dst = OIO_SDS_UPLOAD_DST_INIT;
      ul_dst.url = url;
      gchar data[] = "Content example";

      err = oio_sds_upload_from_buffer(client, &ul_dst, data, sizeof(data));
      oio_url_clean(url);
      g_assert_no_error((GError*)err);

Note that if you try to store an object in a non-existent container, an ``oio_error_s`` is returned.

Retrieving Objects
------------------

Note that if you try to retrieve a non-existent object, an ``oio_error_s`` is returned.

This sample code stores an object and retrieves it using the different parameters.

.. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);
      oio_url_set(url, OIOURL_PATH, "object.txt");

      guchar data[1024];
      struct oio_sds_dl_src_s src = { .url = url, .ranges = NULL };
      struct oio_sds_dl_dst_s dst = {
          .type = OIO_DL_DST_BUFFER,
          .data = {.buffer = {.ptr = data, .length=sizeof(data)}}
      };

      err = oio_sds_download(client, &src, &dst);
      oio_url_clean(url);
      g_assert_no_error((GError*)err);
      g_print("%s", data);

Deleting Objects
----------------

Example:

.. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);
      oio_url_set(url, OIOURL_PATH, "object.txt");

      err = oio_sds_delete(client, url);
      oio_url_clean(url);
      g_assert_no_error((GError*)err);

Note that if you try to delete a non-existent object, an ``oio_error_s`` is returned.

Container and Object Metadata
-----------------------------

The Object Storage API lets you set and retrieve your own metadata on containers and objects.

.. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);

      void _print_element (void *ctx, const char *key, const char *value) {
          (void) ctx;
          g_print("\"%s\": \"%s\", ", key, value);
      }

      g_print("Metadata: {");
      err = oio_sds_get_container_properties(client, url, _print_element, NULL);
      oio_url_clean(url);
      g_assert_no_error((GError*)err);
      g_print("}\n");

It should output an empty dict, unless you added metadata to this container.

.. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);

      const gchar* const properties[5] = {"color", "blue", "flag", "true", NULL};

      err = oio_sds_set_container_properties(client, url, properties);
      g_assert_no_error((GError*)err);

      void _print_element (void *ctx, const char *key, const char *value) {
          (void) ctx;
          g_print("\"%s\": \"%s\", ", key, value);
      }

      g_print("Metadata: {");
      err = oio_sds_get_container_properties(client, url, _print_element, NULL);
      oio_url_clean(url);
      g_assert_no_error((GError*)err);
      g_print("}\n");

It should now output:

.. code-block:: c

      Metadata: {"color": "blue", "flag": "true", }

This is very similar for objects. You can use the methods ``oio_sds_get_content_properties()``
and ``oio_sds_set_content_properties()``.

Listing Objects
---------------

.. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);

      struct oio_sds_list_param_s list_in = {
          .url = url,
          .prefix = NULL, .marker = NULL, .end = NULL, .delimiter = 0, .max_items = 0,
          .flag_allversions = 1, .flag_nodeleted = 1, .flag_properties = 1
      };

      int _print_item (void *ctx, const struct oio_sds_list_item_s *item) {
          (void) ctx;
          g_print("%s\n", item->name);
          return 0;
      }
      struct oio_sds_list_listener_s list_out = {
          .ctx = NULL,
          .on_item = _print_item, .on_prefix = NULL, .on_bound = NULL,
      };

      err = oio_sds_list(client, &list_in, &list_out);
      oio_url_clean(url);
      g_assert_no_error((GError*)err);

This returns a list of objects stored in the container.

Since containers can hold millions of objects, there are several methods to filter the results.

Filters:

- ``marker`` - Indicates where to start the listing from.
- ``end`` - Indicates where to end the listing.
- ``prefix`` - If set, the listing only includes objects whose name begin with its value.
- ``delimiter`` - If set, excludes the objects whose names contain its value. delimiter only takes a single character.
- ``max_items`` - Indicates the maximum number of objects to return in the listing.

To illustrate these features, we can create some objects in a container:

.. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);

      err = oio_sds_create(client, url);
      g_assert_no_error((GError*)err);

      struct oio_sds_ul_dst_s dst = OIO_SDS_UPLOAD_DST_INIT;
      dst.url = url;
      gchar data[] = "sample";

      gchar *name = NULL;
      for (int i = 0; i < 5; i++) {
          name = g_strdup_printf("object%d", i);
          oio_url_set(url, OIOURL_PATH, name);
          err = oio_sds_upload_from_buffer(client, &dst, data, sizeof(data));
          g_free(name);
          g_assert_no_error((GError*)err);
      }

      for (gchar id = 'a'; id <= 'd'; id++) {
          name = g_strdup_printf("foo/%c", id);
          oio_url_set(url, OIOURL_PATH, name);
          err = oio_sds_upload_from_buffer(client, &dst, data, sizeof(data));
          g_free(name);
          g_assert_no_error((GError*)err);
      }

      oio_url_clean(url);

First list all the objects:

.. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);

      struct oio_sds_list_param_s list_in = {
          .url = url,
          .prefix = NULL, .marker = NULL, .end = NULL, .delimiter = 0, .max_items = 0,
          .flag_allversions = 1, .flag_nodeleted = 1, .flag_properties = 1
      };

      int _print_item (void *ctx, const struct oio_sds_list_item_s *item) {
          (void) ctx;
          g_print("%s\n", item->name);
          return 0;
      }
      struct oio_sds_list_listener_s list_out = {
          .ctx = NULL,
          .on_item = _print_item, .on_prefix = NULL, .on_bound = NULL,
      };

      err = oio_sds_list(client, &list_in, &list_out);
      oio_url_clean(url);
      g_assert_no_error((GError*)err);

It should output:

.. code-block:: c

      object4
      object3
      object2
      object1
      object0
      foo/d
      foo/c
      foo/b
      foo/a

Then use the paginating features:

.. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);

      struct oio_sds_list_param_s list_in = {
          .url = url,
          .prefix = NULL, .marker = NULL, .end = NULL, .delimiter = 0, .max_items = 4,
          .flag_allversions = 1, .flag_nodeleted = 1, .flag_properties = 1
      };

      gboolean save_marker;
      gchar marker[16];
      int _print_item (void *ctx, const struct oio_sds_list_item_s *item) {
          (void) ctx;
          g_print("%s, ", item->name);
          if (save_marker) {
              g_strlcpy(marker, item->name, 16);
              save_marker = FALSE;
          }
          return 0;
      }
      struct oio_sds_list_listener_s list_out = {
          .ctx = NULL,
          .on_item = _print_item, .on_prefix = NULL, .on_bound = NULL,
      };

      marker[0] = '\0';
      do {
          g_print("Objects: [");
          save_marker = TRUE;
          list_in.marker = marker;
          err = oio_sds_list(client, &list_in, &list_out);
          g_assert_no_error((GError*)err);
          g_print("]\n");
      } while (list_out.out_count);

      oio_url_clean(url);

Here is the result:

.. code-block:: c

      Objects: [foo/d, foo/c, foo/b, foo/a, ]
      Objects: [object3, object2, object1, object0, ]
      Objects: [object4, ]
      Objects: []

How to use the ``prefix`` parameter:

.. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);

      struct oio_sds_list_param_s list_in = {
          .url = url,
          .prefix = "foo", .marker = NULL, .end = NULL, .delimiter = 0, .max_items = 0,
          .flag_allversions = 1, .flag_nodeleted = 1, .flag_properties = 1
      };

      int _print_item (void *ctx, const struct oio_sds_list_item_s *item) {
          (void) ctx;
          g_print("%s, ", item->name);
          return 0;
      }
      struct oio_sds_list_listener_s list_out = {
          .ctx = NULL,
          .on_item = _print_item, .on_prefix = NULL, .on_bound = NULL,
      };

      g_print("Objects: [");
      err = oio_sds_list(client, &list_in, &list_out);
      oio_url_clean(url);
      g_assert_no_error((GError*)err);
      g_print("]\n");

This only outputs the objects starting with "foo":

.. code-block:: c

      Objects: [foo/d, foo/c, foo/b, foo/a, ]

How to use the ``delimiter`` parameter:

.. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);

      struct oio_sds_list_param_s list_in = {
          .url = url,
          .prefix = NULL, .marker = NULL, .end = NULL, .delimiter = '/', .max_items = 0,
          .flag_allversions = 1, .flag_nodeleted = 1, .flag_properties = 1
      };

      int _print_item (void *ctx, const struct oio_sds_list_item_s *item) {
            (void) ctx;
            g_print("%s, ", item->name);
            return 0;
        }
      struct oio_sds_list_listener_s list_out = {
          .ctx = NULL,
          .on_item = _print_item, .on_prefix = NULL, .on_bound = NULL,
      };

      g_print("Objects: [");
      err = oio_sds_list(client, &list_in, &list_out);
      oio_url_clean(url);
      g_assert_no_error((GError*)err);
      g_print("]\n");

This excludes all the objects in the nested ``foo`` folder.

.. code-block:: c

      Objects: [object4, object3, object2, object1, object0, ]

Note that if you try to list a non-existent container, a ``oio_error_s`` is returned.

Deleting Containers
-------------------

There are several options to delete containers. Example:

.. code-block:: c

      struct oio_url_s *url = oio_url_empty();
      g_assert_nonnull(url);
      oio_url_set(url, OIOURL_NS, NAMESPACE);
      oio_url_set(url, OIOURL_ACCOUNT, ACCOUNT);
      oio_url_set(url, OIOURL_USER, CONTAINER);

      err = oio_sds_delete_container(client, url);
      g_assert_no_error((GError*)err);
      oio_url_clean(url);

You cannot delete a container if it still holds objects, if you try to do so an ``oio_error_s`` is returned.

Note that if you try to delete a non-existent container, a ``oio_error_s`` is returned.
