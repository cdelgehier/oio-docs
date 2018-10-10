Keystone / Swift Integration
============================

Introduction
------------

`Keystone <https://docs.openstack.org/developer/keystone/>`__ is an `Openstack <https://www.openstack.org/>`__ service that provides API client authentication,
service discovery, and distributed multi-tenant authorization by implementing
OpenStack's Identity API.

`Swift <https://docs.openstack.org/developer/swift/>`__ is Openstack's object store.

OpenIO SDS implements the Swift API using the same proxy by replacing the
middleware with one implementing OpenIO SDS API. Used alongside Keystone, it allows administrators
to manage end users' access to data using the Swift API or the S3 API (through the `Swift3 middleware <https://github.com/openstack/swift3>`__).

On the Openstack project website, you will find the full documentation about
`configuring and using Keystone <https://docs.openstack.org/admin-guide/cli-manage-projects-users-and-roles.html>`__. However, since it might appear complex to
administrators to link usage with the object store, this page will help you
understand the basics of using the two solutions together.

Manage accounts
---------------

Accounts are created in Keystone and are then mapped onto Swift. When accessing
a Swift resource, the user authenticates against Keystone, which provides
a token the user will need for each request to Swift. Swift has access to
Keystone to allow or deny each request it receives.

In v2 of `Keystone API v2 <https://developer.openstack.org/api-ref/identity/>`__,
you first create a user, then give a role to that user in a tenant (or
project). The default `domain <https://docs.openstack.org/newton/install-guide-obs/common/glossary.html#term-domain>`__
is *default*.

To create the first user, use the admin token defined in Keystone
configuration. Avoid using these credentials if possible. Get the admin token,
which is defined by the *admin_token* parameter in */etc/keystone/keystone.conf*.
Export it as the *ADMIN_TOKEN* environment variable. Replace *controller* by the IP
address of your Keystone service::

  # export OS_TOKEN=$(awk '/^admin_token/ {print $3}' /etc/keystone/keystone.conf)
  # export OS_URL=http://controller:35357/v2.0
  # export OS_IDENTITY_API_VERSION=2

Next, let's create an *admin* user, put them in the *admin* tenant/project,
and assign to them the *admin* role. The *admin* role is a special role that gives a
user the ability to create entities in Keystone: user, projects, roles, etc.

::

  # openstack project create --description "Admin project" admin
  # openstack user create --password ADMIN_PASS admin
  # openstack role create admin
  # openstack role add --project admin --user admin admin

You can now unset previous environment variables and use the admin user you just
created::

  # unset OS_TOKEN OS_URL OS_IDENTITY_API_VERSION

For ease of use, create a *keystonerc_admin* file containing the admin user
credentials. Be careful with the file access rights::

  # echo 'export OS_TENANT_NAME=admin
  export OS_USERNAME=admin
  export OS_PASSWORD=ADMIN_PASS
  export OS_AUTH_URL=http://controller:5000/v2.0' >keystonerc_admin

Then source the file to be identified as the *admin* user::

  # source keystonerc_admin

Using this account, create another standard account to use with Swift.
Start by creating a project, called *demo* in which you can add a *demo* user with a
*swiftoperator* role::

  # openstack project create demo
  # openstack user create demo --password DEMO_PASS
  # openstack role create swiftoperator
  # openstack role add --project demo --user demo swiftoperator

Now, identifying as the *demo* user, start by creating a file to easily identify::

  # echo 'export OS_TENANT_NAME=demo
  export OS_USERNAME=demo
  export OS_PASSWORD=DEMO_PASS
  export OS_AUTH_URL=http://controller:5000/v2.0' >keystonerc_demo

Source the file, create a container, and add a file in the new
container, checking the information of the account, container, and file, then
download the file pushed. Refer to the `Openstack Swift command line documentation <https://docs.openstack.org/cli-reference/swift.html>`__
for more information on how to use the *swift* command line::

  # source keystonerc_demo
  # swift stat
  # swift post container1
  # swift stat container1
  # swift upload container1 /etc/magic
  # swift stat container1
  # swift stat container1 etc/magic
  # swift download container1 etc/magic

The file is now at the *etc/magic* path; note that uploading the file trimmed
the leading */*.


The default role *_member\_* has no rights to modify Swift containers. The
*swiftoperator* role can give access to *_member\_* users of the project or any
other user of any project using `ACLs <https://docs.openstack.org/developer/swift/overview_acl.html#keystone-auth-acl-elements>`__.

Create another user in the demo project as *admin*::

  # source keystone_admin
  # openstack user create demo2 --password DEMO2_PASS
  # openstack role create _member_
  # openstack role add --project demo --user demo2 _member_

Give read and write privileges to *demo2* using ACLs as *demo* to your
*container1*::

  # source keystone_demo
  # swift post -r 'demo:demo2' -w 'demo:demo2' container1

Next create an authentication file *keystonerc_demo2*::

  # echo 'export OS_TENANT_NAME=demo
  export OS_USERNAME=demo2
  export OS_PASSWORD=DEMO2_PASS
  export OS_AUTH_URL=http://controller:5000/v2.0' >keystonerc_demo2

Source the file and access the object storage::

  # source keystonerc_demo2
  # swift stat container1
  # swift list container1
  # swift upload container1 myfile

Share the container with anyone in read-only::

  # source keystonerc_demo
  # swift post -r '.r:*,.rlistings,demo:demo2' -w 'demo:demo2' container1

To give access to the container and object, you need to share the storage URL;
you can get these using the results of the following command::

  # swift auth

Public users can access the *etc/magic* object in the *container1* using the
*OS_STORAGE_URL* like this::

  # curl -XGET http://controller:6007/v1.0/AUTH_6ff0afaaa43f4e2ba5a4f748b959fa7f/container1/etc/magic

Conclusion
----------

The key idea to understand is that Keystone manages accounts and let users
access project resources in the Swift object store.

Projects can be shared to users with the necessary authorization role in the
same project, and containers can be shared to users of any project, or
publicly to anyone using ACLs.
