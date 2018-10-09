.. title:: Your Swift/S3 backend in a Docker container

.. _ref-docker-image:

============
Docker Image
============

.. contents::
   :backlinks: none
   :depth: 1
   :local:

This `Docker <http://www.docker.com>`_ image provides an easy way to run an OpenIO namespace.
It deploys and configure a simple non-replicated namespace in a single container.

OpenIO SDS service discovery and resolution relies on IP addresses, meaning that you can't change service IPs after they have been registered to the cluster.
By default, Docker networking may change you IP when your container restarts, and this is not compatible with OpenIO SDS at the moment.

Deploy
------

First, download the `OpenIO Docker image <https://hub.docker.com/r/openio/sds/>`_ from the `Docker Hub <https://hub.docker.com>`_:

.. code-block:: console

   # docker pull openio/sds

By default, start a simple namespace listening on 127.0.0.1 inside the container using docker run:

.. code-block:: console

   # docker run -ti --tty openio/sds

You can now manipulate your namespace inside your container using the :ref:`OpenIO End User CLI <ref-user-guide>`. For example, put an object :

.. code-block:: console

   # echo 'Hello OpenIO!' > test.txt

   # openio object create MY_CONTAINER test.txt --oio-ns OPENIO --oio-account MYACCOUNT


Deploy the S3/Swift Gateway
---------------------------

You can launch the OpenIO docker image with our S3 and Swift gateway embedded, and map its port (6007) to access to it remotely.

Launching the container with port mapping:

.. code-block:: console

   # docker run -ti --tty -p 127.0.0.1:6007:6007 openio/sds

The S3 and Swift gateway is now accessible on `127.0.0.1:6007`.

**Using Swift gateway**

First install python-swiftclient:

.. code-block:: console

  # yum install python-swiftclient

Then you can use the swift APIs:

.. code-block:: console

   # swift -A http://127.0.0.1:6007/auth/v1.0/ -U demo:demo -K DEMO_PASS stat

**Using S3 gateway**

First install awscli:

.. code-block:: console

  # yum install awscli

Then, set your credentials in the following configuration file `~/.aws/credentials`:

.. code-block:: console

   [default]
   aws_access_key_id=demo:demo
   aws_secret_access_key=DEMO_PASS
   region=US
   s3 =
       signature_version = s3

Finally you can put your first object:

.. code-block:: console

   # aws --endpoint-url http://127.0.0.1:6007 --no-verify-ssl s3 cp /etc/localtime s3://bucket1

Using the host network interface
--------------------------------

You can start an instance using `Docker host mode networking <https://docs.docker.com/engine/reference/run/#network-host>`_. This allows you to access services outside your container. You can specify the interface or the IP address you want to use.


Setting the interface:

.. code-block:: console

  # docker run -ti --tty -e OPENIO_IFDEV=enp0s8 --net=host openio/sds

Specifying the IP:

.. code-block:: console

  # docker run -ti --tty -e OPENIO_IPADDR=192.168.56.101 --net=host openio/sds
