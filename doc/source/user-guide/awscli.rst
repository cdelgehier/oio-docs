==========
AWS S3 CLI
==========

This guide provides a few tips to help users get started with the `AWS S3 command line client`_ using the OpenIO Swift gateway. By default, the gateway uses the Swift3 middleware to allow access to OpenIO object storage using the Amazon S3 API.
The AWS CLI allows you to use the different APIs provided by AWS, including the `S3`_ and `S3API`_ ones.

Configuration
=============

Client configuration depends on whether you use a `TempAuth`_ or `Keystone`_ authentication on the Swift proxy.

TempAuth
--------

To use the AWS command, you need to set your credentials in the `~/.aws/credentials` file:

   .. code-block:: console

      # mkdir ~/.aws
      # echo "[default]
      aws_access_key_id=demo:demo
      aws_secret_access_key=DEMO_PASS" >~/.aws/credentials

You can also set specific parameters for the S3 commands:

   .. code-block:: console

     # echo "[default]
     region = us-east-1
     s3 =
      signature_version = s3v4
      max_concurrent_requests = 10
      max_queue_size = 100
      multipart_threshold = 1GB
      multipart_chunksize = 10MB" >~/.aws/config

Keystone
--------

Using the Openstack Keystone authentication system, you need to obtain a token in order in order to authenticate.
You need to install the `Openstack command line interface`_.
Export these variables to use the S3 CLI. Create a file `~/keystonerc_demo` containing:

   .. code-block:: console
      :caption: Required environment

    export OS_TENANT_NAME=demo
    export OS_USERNAME=demo
    export OS_PASSWORD=DEMO_PASS
    export OS_AUTH_URL=http://localhost:5000/v2.0

  .. Note:: Replace the IP with the IP address of your Keystone service

Source your credentials and get a token:

   .. code-block:: console

    # . keystonerc_demo ; openstack ec2 credentials create

Configure your credentials to *~/.aws/credantials* and configure the default S3 client.
Replace *ACCESS_KEY* and *SECRET_KEY* with the result of the previous command:

   .. code-block:: console

    # mkdir ~/.aws
    # vi ~/.aws/credentials

   .. code-block:: console
      :caption: ~/.aws/credentials

    [default]
    aws_access_key_id=ACCESS_KEY
    aws_secret_access_key=SECRET_KEY

   .. code-block:: console

    # vi ~/.aws/config

   .. code-block:: console
      :caption: ~/.aws/config

    [default]
    region = us-east-1
    s3 =
      signature_version = s3v4
      max_concurrent_requests = 20
      max_queue_size = 100
      multipart_threshold = 10GB
      multipart_chunksize = 10MB

Usage
=====

You will need to provide the command line the endpoint of the Swift gateway and disable SSL verification, as it is not provided by default.

.. note:: Replace *localhost* with the IP address of your OpenIO Swift proxy.

Install awscli
--------------

  .. code-block:: console

    # yum install awscli

Create a bucket
---------------

  .. code-block:: console

    # aws --endpoint-url http://localhost:6007 --no-verify-ssl s3 mb s3://test1

List buckets
------------

  .. code-block:: console

    # aws --endpoint-url http://localhost:6007 --no-verify-ssl s3 ls

Upload content
--------------

  .. code-block:: console

    # aws --endpoint-url http://localhost:6007 --no-verify-ssl s3 cp /etc/magic s3://test1


.. _AWS S3 command line client: https://aws.amazon.com/cli/
.. _S3: http://docs.aws.amazon.com/cli/latest/reference/s3/
.. _S3API: http://docs.aws.amazon.com/cli/latest/reference/s3api/
.. _TempAuth: https://docs.openstack.org/developer/swift/overview_auth.html#tempauth
.. _Keystone: https://docs.openstack.org/developer/keystone/
.. _Swift3: https://github.com/openstack/swift3
.. _Openstack command line interface: https://docs.openstack.org/user-guide/common/cli-install-openstack-command-line-clients.html
