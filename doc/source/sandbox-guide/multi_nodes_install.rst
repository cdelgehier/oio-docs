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

-  root privileges are required (using sudo)

-  `SELinux <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-working_with_selinux-changing_selinux_modes>`__ or `AppArmor <https://help.ubuntu.com/lts/serverguide/apparmor.html.en>`__ are disabled

  .. code-block:: shell

    # RedHat
    sudo sed -i -e 's@^SELINUX=enforcing$@SELINUX=disabled@g' /etc/selinux/config
    sudo setenforce 0
    sudo systemctl disable selinux.service

  .. code-block:: shell

    # Ubuntu
    sudo systemctl stop apparmor.service
    sudo update-rc.d -f apparmor remove

-  All nodes must have different hostnames
-  ``/var/lib`` partition must support Extended Attributes: XFS is recommended

  .. code-block:: shell

    [root@centos ~]# df /var/lib
    Filesystem     1K-blocks    Used Available Use% Mounted on
    /dev/vda1       41931756 1624148  40307608   4% /
    [root@centos ~]# file -sL /dev/vda1
    /dev/vda1: SGI XFS filesystem data (blksz 4096, inosz 512, v2 dirs)

-  System must be up-to-date

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

    # RedHat
    sudo systemctl stop firewalld.service
    sudo systemctl disable firewalld.service

  .. code-block:: shell

    # Ubuntu
    sudo sudo ufw disable
    sudo systemctl disable ufw.service


Setup
-----

You only need to perform this setup on one of the node involved in the cluster (or your laptop)

-  Install Ansible (versions 2.4 or 2.5) (`official guide <https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html>`__)
-  Install ``git`` and ``python-netaddr``

  .. code-block:: shell

    # RedHat
    sudo yum install git python-netaddr -y

  .. code-block:: shell

    # Ubuntu
    sudo apt install git python-netaddr -y

-  Clone the OpenIO ansible playbook deployment repository

  .. code-block:: shell

    git clone https://github.com/open-io/ansible-playbook-openio-deployment.git oiosds && cd oiosds/products/sds

Architecture
============

This playbook will deploy a multi nodes cluster as below

  .. code-block:: shell

    +-----------------+   +-----------------+   +-----------------+
    |     KEYSTONE    |   |     KEYSTONE    |   |     KEYSTONE    |
    |                 |   |                 |   |                 |
    +-----------------+   +-----------------+   +-----------------+
    |     DATABASE    |   |     DATABASE    |   |     DATABASE    |
    +-----------------+   +-----------------+   +-----------------+
    |     OIOSWIFT    |   |     OIOSWIFT    |   |     OIOSWIFT    |
    |                 |   |                 |   |                 |
    +-----------------+   +-----------------+   +-----------------+
    |      OPENIO     |   |      OPENIO     |   |      OPENIO     |
    |       SDS       |   |       SDS       |   |       SDS       |
    +-----------------+   +-----------------+   +-----------------+



Installation
============

First you need to fill the inventory accordingly to your environment:

- Edit the ``inventories/n-nodes/01_inventory.ini`` file and adapt the IP addresses and SSH user (sample here: `inventory <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/n-nodes/01_inventory.ini>`__)

  .. code-block:: shell

    [all]
    node1 ansible_host=10.0.0.1 # Change it with the IP of the first server
    node2 ansible_host=10.0.0.2 # Change it with the IP of the second server
    node3 ansible_host=10.0.0.3 # Change it with the IP of the third server
    ...

  .. code-block:: shell

    [all:vars]
    ansible_user=root # Change it accordingly

If you need a custom deployment (per node typically): you can override the default values in each file ``host_vars/nodeX.yml`` like `here <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/n-nodes/host_vars/node1.yml>`__.

.. code-block:: shell

  [all]
  node1 ansible_host=10.0.0.1 # Change it with the IP of the first server
  node2 ansible_host=10.0.0.2 # Change it with the IP of the second server
  node3 ansible_host=10.0.0.3 # Change it with the IP of the third server
  ...

You can check that everything is well configured using this command:

  .. code-block:: shell

    ansible all -i inventories/n-nodes -bv -m ping

Run these commands:

-  To download and install requirements:

  .. code-block:: shell

    ./requirements_install.sh

- To deploy:

  .. code-block:: shell

    ansible-playbook -i inventories/n-nodes main.yml

Post-install Checks
===================

All the nodes are configured to easily use the openio-cli and aws-cli.

Run this check script on one of the node involved in the cluster ``sudo /root/checks.sh``

Sample output:

::

  [centos@node1 ~]$ sudo /root/checks.sh
  ## OPENIO
   Status of services.
  KEY                       STATUS      PID GROUP
  OPENIO-account-0          UP         5604 OPENIO,account,0
  OPENIO-beanstalkd-1       UP         7513 OPENIO,beanstalkd,beanstalkd-1
  OPENIO-conscienceagent-1  UP         7498 OPENIO,conscienceagent,conscienceagent-1
  OPENIO-ecd-0              UP         9633 OPENIO,ecd,0
  OPENIO-keystone-0.0       UP        13469 OPENIO,keystone,0,keystone-wsgi-public
  OPENIO-keystone-0.1       UP        13454 OPENIO,keystone,0,keystone-wsgi-admin
  OPENIO-memcached-0        UP        10415 OPENIO,memcached,0
  OPENIO-meta0-1            UP         8388 OPENIO,meta0,meta0-1
  OPENIO-meta1-1            UP         8412 OPENIO,meta1,meta1-1
  OPENIO-meta2-1            UP         7602 OPENIO,meta2,meta2-1
  OPENIO-oio-blob-indexer-1 UP         7603 OPENIO,oio-blob-indexer,oio-blob-indexer-1
  OPENIO-oio-event-agent-0  UP         7504 OPENIO,oio-event-agent,oio-event-agent-0
  OPENIO-oioproxy-1         UP         7697 OPENIO,oioproxy,oioproxy-1
  OPENIO-oioswift-0         UP        14856 OPENIO,oioswift,0
  OPENIO-rawx-1             UP         7585 OPENIO,rawx,rawx-1
  OPENIO-rdir-1             UP         7689 OPENIO,rdir,rdir-1
  OPENIO-redis-1            UP         7573 OPENIO,redis,redis-1
  OPENIO-redissentinel-1    UP         7558 OPENIO,redissentinel,redissentinel-1
  OPENIO-zookeeper-0        UP         4811 OPENIO,zookeeper,0
  --
   Display the cluster status.
  +---------+-----------------+------------+---------------------------------+--------------+-------+------+-------+
  | Type    | Addr            | Service Id | Volume                          | Location     | Slots | Up   | Score |
  +---------+-----------------+------------+---------------------------------+--------------+-------+------+-------+
  | account | 172.17.0.2:6009 | n/a        | n/a                             | 5bdc8fbc3ceb | n/a   | True |    95 |
  | account | 172.17.0.3:6009 | n/a        | n/a                             | 60b8ffa564c4 | n/a   | True |    95 |
  | account | 172.17.0.4:6009 | n/a        | n/a                             | 3b7bf6e74c6c | n/a   | True |    95 |
  | meta0   | 172.17.0.2:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | 5bdc8fbc3ceb | n/a   | True |    97 |
  | meta0   | 172.17.0.3:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | 60b8ffa564c4 | n/a   | True |    97 |
  | meta0   | 172.17.0.4:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | 3b7bf6e74c6c | n/a   | True |    97 |
  | meta1   | 172.17.0.2:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | 5bdc8fbc3ceb | n/a   | True |    72 |
  | meta1   | 172.17.0.3:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | 60b8ffa564c4 | n/a   | True |    72 |
  | meta1   | 172.17.0.4:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | 3b7bf6e74c6c | n/a   | True |    72 |
  | meta2   | 172.17.0.2:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | 5bdc8fbc3ceb | n/a   | True |    72 |
  | meta2   | 172.17.0.3:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | 60b8ffa564c4 | n/a   | True |    72 |
  | meta2   | 172.17.0.4:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | 3b7bf6e74c6c | n/a   | True |    72 |
  | rawx    | 172.17.0.2:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | 5bdc8fbc3ceb | n/a   | True |    72 |
  | rawx    | 172.17.0.3:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | 60b8ffa564c4 | n/a   | True |    72 |
  | rawx    | 172.17.0.4:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | 3b7bf6e74c6c | n/a   | True |    72 |
  | rdir    | 172.17.0.2:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | 5bdc8fbc3ceb | n/a   | True |    95 |
  | rdir    | 172.17.0.3:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | 60b8ffa564c4 | n/a   | True |    95 |
  | rdir    | 172.17.0.4:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | 3b7bf6e74c6c | n/a   | True |    95 |
  +---------+-----------------+------------+---------------------------------+--------------+-------+------+-------+
  --
   Upload the /etc/passwd into the bucket MY_CONTAINER of the MY_ACCOUNT project.
  +--------+------+----------------------------------+--------+
  | Name   | Size | Hash                             | Status |
  +--------+------+----------------------------------+--------+
  | passwd | 1273 | 217F67C9C35A6C84B58B852DBF0C4BA2 | Ok     |
  +--------+------+----------------------------------+--------+
  --
   Get some informations about your object.
  +----------------+--------------------------------------------------------------------+
  | Field          | Value                                                              |
  +----------------+--------------------------------------------------------------------+
  | account        | MY_ACCOUNT                                                         |
  | base_name      | 7B1F1716BE955DE2D677B68819836E4F75FD2424F6D22DB60F9F2BB40331A741.1 |
  | bytes_usage    | 1.273KB                                                            |
  | container      | MY_CONTAINER                                                       |
  | ctime          | 1530454404                                                         |
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
  | passwd | 1273 | 217F67C9C35A6C84B58B852DBF0C4BA2 | 1530454404437338 |
  +--------+------+----------------------------------+------------------+
  --
   Find the services involved for your container.
  +-----------+--------------------------------------------------------------------+
  | Field     | Value                                                              |
  +-----------+--------------------------------------------------------------------+
  | account   | MY_ACCOUNT                                                         |
  | base_name | 7B1F1716BE955DE2D677B68819836E4F75FD2424F6D22DB60F9F2BB40331A741.1 |
  | meta0     | 172.17.0.2:6001, 172.17.0.3:6001, 172.17.0.4:6001                  |
  | meta1     | 172.17.0.2:6111, 172.17.0.3:6111, 172.17.0.4:6111                  |
  | meta2     | 172.17.0.4:6121, 172.17.0.3:6121, 172.17.0.2:6121                  |
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
  2018-07-01 16:13:30    1.2 KiB passwd

  Total Objects: 1
     Total Size: 1.2 KiB
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


Disclaimer
==========

Please keep in mind that this guide is not intended for production, use it for demo/POC/development purposes only.

**Don't go in production with this setup.**
