.. _label-swift-cli-example:

===================
Openstack Swift CLI
===================

.. contents::
   :backlinks: none
   :depth: 1
   :local:

This guide provides a few tips to help users getting started with the Openstack Swift command line client.
The Openstack Swift command line client supports different authentication methods; the way to use the client
depends on how the OpenIO Swift gateway is deployed.

TempAuth
========

TempAuth is used on test environments; it is a simple way to try out Swift.
You will need the Swift endpoint address and the port of the OpenIO Swift gateway (the default port is 6007).
The user is defined as *project*:*user*.
In OpenIO SDS, simply check the account information:

   .. code-block:: console

    # swift -A http://127.0.0.1:6007/auth/v1.0/ -U demo:demo -K DEMO_PASS stat


Keystone
========

In production environments, it is recommended to use Openstack Keystone to authenticate your users.
You will need the Keystone endpoint URL (the default port is 5000) as well as a project (or tenant), username and password. It is common use to create a file *keystonerc_username* with the following content:

   .. code-block:: console
     :caption: keystone v2

     export OS_TENANT_NAME=demo
     export OS_USERNAME=demo
     export OS_PASSWORD=DEMO_PASS
     export OS_AUTH_URL=http://127.0.0.1:5000/v2.0


   .. code-block:: console
     :caption: keystone v3

     export OS_PROJECT_DOMAIN_NAME=default
     export OS_USER_DOMAIN_NAME=default
     export OS_PROJECT_NAME=demo
     export OS_USERNAME=demo
     export OS_PASSWORD=DEMO_PASS
     export OS_AUTH_URL=http://127.0.0.1:5000/v3
     export OS_IDENTITY_API_VERSION=3
     export OS_IMAGE_API_VERSION=2


Source the file:

   .. code-block:: console

     # source keystonerc_demo

You can check the account information using the stat command:

   .. code-block:: console

     # swift stat
