.. _ref-install-guide:
========================
Multi Nodes Installation
========================

.. contents::
   :depth: 1
   :local:

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

-  Root privileges are required (using sudo).
-  `SELinux <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-working_with_selinux-changing_selinux_modes>`__ or `AppArmor <https://help.ubuntu.com/lts/serverguide/apparmor.html.en>`__ are disabled (managed at deployment).
-  All nodes must have different hostnames.
-  The ``/var/lib`` partition must support extended attributes: XFS is recommended.

  .. code-block:: shell

    [root@centos ~]# df /var/lib
    Filesystem     1K-blocks    Used Available Use% Mounted on
    /dev/vda1       41931756 1624148  40307608   4% /
    [root@centos ~]# file -sL /dev/vda1
    /dev/vda1: SGI XFS filesystem data (blksz 4096, inosz 512, v2 dirs)

-  The system must be up to date.

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

-  All nodes are connected to the same LAN through the specified interface (first one by default).
-  The firewall is disabled (managed at deployment).

  .. code-block:: shell

    # Ubuntu
    sudo sudo ufw disable
    sudo systemctl disable ufw.service


Setup
-----

You only need to perform this setup on one of the nodes in the cluster (or your laptop).

-  Install Ansible (`official guide <https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html>`__).
-  Install ``git`` and ``python-netaddr`` (this one is managed at deployment).

  .. code-block:: shell

    # RedHat
    sudo yum install git -y

  .. code-block:: shell

    # Ubuntu
    sudo apt install git -y

-  Clone the OpenIO ansible playbook deployment repository

  .. code-block:: shell

    git clone https://github.com/open-io/ansible-playbook-openio-deployment.git oiosds && cd oiosds/products/sds

Architecture
============

This playbook will deploy a multi-nodes cluster as shown below:

  .. code-block:: shell


    +-----------------+   +-----------------+   +-----------------+
    |     OIOSWIFT    |   |     OIOSWIFT    |   |     OIOSWIFT    |
    |      FOR S3     |   |      FOR S3     |   |      FOR S3     |
    +-----------------+   +-----------------+   +-----------------+
    |      OPENIO     |   |      OPENIO     |   |      OPENIO     |
    |       SDS       |   |       SDS       |   |       SDS       |
    +-----------------+   +-----------------+   +-----------------+



Installation
============

First, fill the inventory according to your environment:

- Edit the ``inventories/n-nodes/01_inventory.ini`` file and adapt the IP addresses and SSH user (sample here: `inventory <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/n-nodes/01_inventory.ini>`__).

  .. code-block:: shell

    [all]
    node1 ansible_host=10.0.0.1 # Change it with the IP of the first server
    node2 ansible_host=10.0.0.2 # Change it with the IP of the second server
    node3 ansible_host=10.0.0.3 # Change it with the IP of the third server
    ...

  .. code-block:: shell

    [all:vars]
    ansible_user=root # Change it accordingly

You can check that everything is configured correctly using this command:

  .. code-block:: shell

    ansible all -i inventories/n-nodes -bv -m ping

Run these commands:

-  To download and install requirements:

  .. code-block:: shell

    ./requirements_install.sh

- To deploy:

  .. code-block:: shell

    ansible-playbook -i inventories/n-nodes main.yml

Post-installation Checks
========================

All the nodes are configured to use openio-cli and aws-cli.

Run this check script on one of the nodes in the cluster ``sudo /root/checks.sh``.

Sample output:

::

  [root@node1 ~]# ./checks.sh
  ## OPENIO
   Status of services.
  KEY                       STATUS      PID GROUP
  OPENIO-account-0          UP         2585 OPENIO,account,0
  OPENIO-beanstalkd-1       UP         4932 OPENIO,beanstalkd,beanstalkd-1
  OPENIO-conscienceagent-1  UP         4916 OPENIO,conscienceagent,conscienceagent-1
  OPENIO-ecd-0              UP         7303 OPENIO,ecd,0
  OPENIO-memcached-0        UP         7706 OPENIO,memcached,0
  OPENIO-meta0-1            UP         5977 OPENIO,meta0,meta0-1
  OPENIO-meta1-1            UP         5994 OPENIO,meta1,meta1-1
  OPENIO-meta2-1            UP         5111 OPENIO,meta2,meta2-1
  OPENIO-oio-blob-indexer-1 UP         5091 OPENIO,oio-blob-indexer,oio-blob-indexer-1
  OPENIO-oio-event-agent-0  UP         4985 OPENIO,oio-event-agent,oio-event-agent-0
  OPENIO-oioproxy-1         UP         5112 OPENIO,oioproxy,oioproxy-1
  OPENIO-oioswift-0         UP         9163 OPENIO,oioswift,0
  OPENIO-rawx-1             UP         5005 OPENIO,rawx,rawx-1
  OPENIO-rdir-1             UP         5108 OPENIO,rdir,rdir-1
  OPENIO-redis-1            UP         5002 OPENIO,redis,redis-1
  OPENIO-redissentinel-1    UP         4984 OPENIO,redissentinel,redissentinel-1
  OPENIO-zookeeper-0        UP         3914 OPENIO,zookeeper,0
  --
   Display the cluster status.
  +---------+-----------------+------------+---------------------------------+----------+-------+------+-------+
  | Type    | Addr            | Service Id | Volume                          | Location | Slots | Up   | Score |
  +---------+-----------------+------------+---------------------------------+----------+-------+------+-------+
  | account | 172.17.0.4:6009 | n/a        | n/a                             | node3    | n/a   | True |    98 |
  | account | 172.17.0.3:6009 | n/a        | n/a                             | node2    | n/a   | True |    96 |
  | account | 172.17.0.2:6009 | n/a        | n/a                             | node1    | n/a   | True |    98 |
  | meta0   | 172.17.0.3:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | node2    | n/a   | True |    99 |
  | meta0   | 172.17.0.4:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | node3    | n/a   | True |    99 |
  | meta0   | 172.17.0.2:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | node1    | n/a   | True |    99 |
  | meta1   | 172.17.0.3:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | node2    | n/a   | True |    69 |
  | meta1   | 172.17.0.4:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | node3    | n/a   | True |    69 |
  | meta1   | 172.17.0.2:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | node1    | n/a   | True |    69 |
  | meta2   | 172.17.0.3:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | node2    | n/a   | True |    69 |
  | meta2   | 172.17.0.4:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | node3    | n/a   | True |    69 |
  | meta2   | 172.17.0.2:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | node1    | n/a   | True |    69 |
  | rawx    | 172.17.0.3:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | node2    | n/a   | True |    69 |
  | rawx    | 172.17.0.4:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | node3    | n/a   | True |    69 |
  | rawx    | 172.17.0.2:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | node1    | n/a   | True |    69 |
  | rdir    | 172.17.0.3:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | node2    | n/a   | True |    98 |
  | rdir    | 172.17.0.4:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | node3    | n/a   | True |    98 |
  | rdir    | 172.17.0.2:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | node1    | n/a   | True |    98 |
  +---------+-----------------+------------+---------------------------------+----------+-------+------+-------+
  --
   Upload the /etc/passwd file to the bucket MY_CONTAINER of the project MY_ACCOUNT.
  +--------+------+----------------------------------+--------+
  | Name   | Size | Hash                             | Status |
  +--------+------+----------------------------------+--------+
  | passwd | 1246 | D39F219BF5875D561DAFB2B789CD1C6C | Ok     |
  +--------+------+----------------------------------+--------+
  --
   Get some information about your object.
  +----------------+--------------------------------------------------------------------+
  | Field          | Value                                                              |
  +----------------+--------------------------------------------------------------------+
  | account        | MY_ACCOUNT                                                         |
  | base_name      | 7B1F1716BE955DE2D677B68819836E4F75FD2424F6D22DB60F9F2BB40331A741.1 |
  | bytes_usage    | 1.246KB                                                            |
  | container      | MY_CONTAINER                                                       |
  | ctime          | 1532608812                                                         |
  | max_versions   | Namespace default                                                  |
  | objects        | 1                                                                  |
  | quota          | Namespace default                                                  |
  | status         | Enabled                                                            |
  | storage_policy | Namespace default                                                  |
  +----------------+--------------------------------------------------------------------+
  --
   List the object in its container.
  +--------+------+----------------------------------+------------------+
  | Name   | Size | Hash                             |          Version |
  +--------+------+----------------------------------+------------------+
  | passwd | 1246 | D39F219BF5875D561DAFB2B789CD1C6C | 1532608905500461 |
  +--------+------+----------------------------------+------------------+
  --
   Find the services involved for your container.
  +-----------+--------------------------------------------------------------------+
  | Field     | Value                                                              |
  +-----------+--------------------------------------------------------------------+
  | account   | MY_ACCOUNT                                                         |
  | base_name | 7B1F1716BE955DE2D677B68819836E4F75FD2424F6D22DB60F9F2BB40331A741.1 |
  | meta0     | 172.17.0.3:6001, 172.17.0.4:6001, 172.17.0.2:6001                  |
  | meta1     | 172.17.0.2:6111, 172.17.0.3:6111, 172.17.0.4:6111                  |
  | meta2     | 172.17.0.4:6121, 172.17.0.2:6121, 172.17.0.3:6121                  |
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
   AWSCli credentials used.
  [default]
  aws_access_key_id = demo:demo
  aws_secret_access_key = DEMO_PASS
  --
   Create a bucket mybucket.
  make_bucket: mybucket
  --
   Upload the /etc/passwd file to the bucket mybucket.
  upload: ../etc/passwd to s3://mybucket/passwd
  --
   List your buckets.
  2018-07-26 14:41:48    1.2 KiB passwd

  Total Objects: 1
     Total Size: 1.2 KiB
  --
   Save the data stored in the given object to the given file.
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


.. include:: manual_requirements.rst

.. include:: custom_deployment.rst
