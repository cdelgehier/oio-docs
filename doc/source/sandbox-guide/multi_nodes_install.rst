===================
Multi nodes install
===================

Requirements
============

Hardware
--------

-  RAM: 2GB recommended

Operating system
----------------

-  Centos 7
-  Ubuntu 16.04 (Server)

System
------

-  `SELinux <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-working_with_selinux-changing_selinux_modes>`__ or `AppArmor <https://help.ubuntu.com/lts/serverguide/apparmor.html.en>`__ are disabled

  .. code-block:: shell

    # RedHat
    sudo sed -i -e 's@^SELINUX=enforcing$@SELINUX=disabled@g' /etc/selinux/config
    sudo setenforce 0
    sudo systemctl disable selinux.service

  .. code-block:: shell

    # Ubuntu
    sudo systemctl stop apparmor.service
    sudo systemctl disable apparmor.service

-  root privileges are required (using sudo)

  .. code-block:: shell

    # MYUSER    ALL=(ALL)    NOPASSWD: ALL

-  All nodes must have different hostnames
-  ``/var/lib`` partition must support Extended Attributes: XFS is recommended

  .. code-block:: shell

    [root@centos ~]# df /var/lib
    Filesystem     1K-blocks    Used Available Use% Mounted on
    /dev/vda1       41931756 1624148  40307608   4% /
    [root@centos ~]# file -sL /dev/vda1
    /dev/vda1: SGI XFS filesystem data (blksz 4096, inosz 512, v2 dirs)
-  All have to be up-to-date

  .. code-block:: shell

    # RedHat
    sudo yum update -y
    sudo reboot

  .. code-block:: shell

    # Ubuntu
    sudo apt update -y
    sudo apt upgrade -y
    sudo reboot

Network
-------

-  All nodes connected to the same LAN through the specified interface (first one by default)
-  Firewall is disabled

  .. code-block:: shell

    sudo systemctl stop firewalld.service
    sudo systemctl disable firewalld.service


Setup
-----

-  Clone this repository (or download it with wget and unzip)

  .. code-block:: shell

    git clone https://github.com/open-io/ansible-playbook-openio-deployment.git oiosds


-  Install Ansible as `describe <https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html>`__
-  Install git for download requirements
-  Install ``python-netaddr``



Architecture
============

You have to choose your POC architecture:

- N-Node (at least 3) for a storage policy in '3 copies'
- Standalone node (all in one)

Installation
============

After filling the inventory corresponding to your choice :

- For a N/3 nodes :

  - `inventory <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/n-nodes/01_inventory.ini>`__ (Adapt IP address and user ssh)
  - `OpenIO configuration <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/n-nodes/group_vars/openio.yml>`__
- For a uniq node :

  - `inventory <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/standalone/01_inventory.ini>`__ (Adapt IP address and user ssh)
  - `OpenIO configuration <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/standalone/group_vars/openio.yml>`__

You can check your customization like this:

.. code-block:: shell

  ansible all -i inventories/<YOUR_CHOICE> -bv -m ping

You can run these commands:

- For download requirements:

  .. code-block:: shell

      ./requirements_install.sh

- For deploy:

  .. code-block:: shell

    ansible-playbook -i inventories/<YOUR_CHOICE> main.yml

Test
====

All the nodes are configured to easily use the openio-cli and aws-cli.

Log you into one node and look at the file ``/root/checks.sh``


Sample output:


::

    [root@node1 ~]# ./checks.sh
    ## OPENIO
     Display the cluster status.
    +---------+-----------------+------------+---------------------------------+----------+-------+------+-------+
    | Type    | Addr            | Service Id | Volume                          | Location | Slots | Up   | Score |
    +---------+-----------------+------------+---------------------------------+----------+-------+------+-------+
    | account | 10.0.0.187:6009 | n/a        | n/a                             | test-3   | n/a   | True |    99 |
    | account | 10.0.0.184:6009 | n/a        | n/a                             | test-1   | n/a   | True |    99 |
    | account | 10.0.0.185:6009 | n/a        | n/a                             | test-2   | n/a   | True |    99 |
    | meta0   | 10.0.0.187:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | test-3   | n/a   | True |    99 |
    | meta0   | 10.0.0.184:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | test-1   | n/a   | True |    99 |
    | meta0   | 10.0.0.185:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | test-2   | n/a   | True |    99 |
    | meta1   | 10.0.0.187:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | test-3   | n/a   | True |    98 |
    | meta1   | 10.0.0.184:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | test-1   | n/a   | True |    98 |
    | meta1   | 10.0.0.185:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | test-2   | n/a   | True |    98 |
    | meta2   | 10.0.0.187:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | test-3   | n/a   | True |    98 |
    | meta2   | 10.0.0.184:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | test-1   | n/a   | True |    98 |
    | meta2   | 10.0.0.185:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | test-2   | n/a   | True |    98 |
    | rawx    | 10.0.0.187:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | test-3   | n/a   | True |    98 |
    | rawx    | 10.0.0.184:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | test-1   | n/a   | True |    98 |
    | rawx    | 10.0.0.185:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | test-2   | n/a   | True |    98 |
    | rdir    | 10.0.0.187:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | test-3   | n/a   | True |    99 |
    | rdir    | 10.0.0.184:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | test-1   | n/a   | True |    99 |
    | rdir    | 10.0.0.185:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | test-2   | n/a   | True |    99 |
    +---------+-----------------+------------+---------------------------------+----------+-------+------+-------+
    --
     Upload the /etc/passwd into the bucket MY_CONTAINER of the MY_ACCOUNT project.
    +--------+------+----------------------------------+--------+
    | Name   | Size | Hash                             | Status |
    +--------+------+----------------------------------+--------+
    | passwd | 1730 | 9993F77821043A9F5EF7625CCD3A49FC | Ok     |
    +--------+------+----------------------------------+--------+
    --
     Get some informations about your object.
    +----------------+--------------------------------------------------------------------+
    | Field          | Value                                                              |
    +----------------+--------------------------------------------------------------------+
    | account        | MY_ACCOUNT                                                         |
    | base_name      | 7B1F1716BE955DE2D677B68819836E4F75FD2424F6D22DB60F9F2BB40331A741.1 |
    | bytes_usage    | 1.73KB                                                             |
    | container      | MY_CONTAINER                                                       |
    | ctime          | 1530281508                                                         |
    | max_versions   | Namespace default                                                  |
    | objects        | 1                                                                  |
    | quota          | Namespace default                                                  |
    | status         | Enabled                                                            |
    | storage_policy | Namespace default                                                  |
    +----------------+--------------------------------------------------------------------+
    --
     List object in container.
    +--------+------+----------------------------------+------------------+
    | Name   | Size | Hash                             |          Version |
    +--------+------+----------------------------------+------------------+
    | passwd | 1730 | 9993F77821043A9F5EF7625CCD3A49FC | 1530281508164444 |
    +--------+------+----------------------------------+------------------+
    --
     Find the services involved for your container.
    +-----------+--------------------------------------------------------------------+
    | Field     | Value                                                              |
    +-----------+--------------------------------------------------------------------+
    | account   | MY_ACCOUNT                                                         |
    | base_name | 7B1F1716BE955DE2D677B68819836E4F75FD2424F6D22DB60F9F2BB40331A741.1 |
    | meta0     | 10.0.0.187:6001, 10.0.0.184:6001, 10.0.0.185:6001                  |
    | meta1     | 10.0.0.184:6111, 10.0.0.185:6111, 10.0.0.187:6111                  |
    | meta2     | 10.0.0.187:6121, 10.0.0.184:6121, 10.0.0.185:6121                  |
    | name      | MY_CONTAINER                                                       |
    | status    | Enabled                                                            |
    +-----------+--------------------------------------------------------------------+
    --
     Save the data stored in the given object to the --file destination.
    root:x:0:0:root:/root:/bin/bash
    bin:x:1:1:bin:/bin:/sbin/nologin
    daemon:x:2:2:daemon:/sbin:/sbin/nologin
    adm:x:3:4:adm:/var/adm:/sbin/nologin
    lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
    sync:x:5:0:sync:/sbin:/bin/sync
    shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
    halt:x:7:0:halt:/sbin:/sbin/halt
    mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
    operator:x:11:0:operator:/root:/sbin/nologin
    --
     Delete your object.
    +--------+---------+
    | Name   | Deleted |
    +--------+---------+
    | passwd | True    |
    +--------+---------+
    --
     Delete your empty container.
    --

    ------
    ## AWS
     Create a bucket mybucket.
    make_bucket: mybucket
    --
     Upload the /etc/passwd into the bucket mybucket.
    upload: ../etc/passwd to s3://mybucket/passwd
    --
     List your buckets.
    2018-06-29 16:11:51    1.7 KiB passwd

    Total Objects: 1
       Total Size: 1.7 KiB
    --
     Save the data stored in the given object into the file given.
    download: s3://mybucket/passwd to ../tmp/passwd.aws
    root:x:0:0:root:/root:/bin/bash
    bin:x:1:1:bin:/bin:/sbin/nologin
    daemon:x:2:2:daemon:/sbin:/sbin/nologin
    adm:x:3:4:adm:/var/adm:/sbin/nologin
    lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
    sync:x:5:0:sync:/sbin:/bin/sync
    shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
    halt:x:7:0:halt:/sbin:/sbin/halt
    mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
    operator:x:11:0:operator:/root:/sbin/nologin
    --
     Delete your object.
    delete: s3://mybucket/passwd
    --
     Delete your empty bucket.
    remove_bucket: mybucket

    Done

Low capacity nodes
==================

For many use cases (ARM, docker, ...), it can be useful to reduce the consumption of some components.
In the `group\_vars\/openio.yml <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/n-nodes/group_vars/openio.yml>`__ , you'll find a section to uncomment.

Disclaimer
==========

Please keep in mind that deployment allows you to install OpenIO for demo/POC/development purposes only.

Don't go in production with this setup.

