===================
Single node install
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
-  `SELinux <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-working_with_selinux-changing_selinux_modes>`__ or `AppArmor <https://help.ubuntu.com/lts/serverguide/apparmor.html.en>`__ are disabled (managed at deployment)
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

-  Firewall is disabled (managed at deployment)

Setup
-----

You only need to perform this setup on one of the node involved in the cluster (or your laptop)

-  Install Ansible (`official guide <https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html>`__)
-  Install ``git`` and ``python-netaddr`` (this one is managed at deployment)

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

This playbook will deploy a multi nodes cluster as below

  .. code-block:: shell

    +-----------------+
    |     OIOSWIFT    |
    |      FOR S3     |
    +-----------------+
    |      OPENIO     |
    |       SDS       |
    +-----------------+

Installation
============

First you need to fill the inventory accordingly to your environment:

- Edit the ``inventories/standalone/01_inventory.ini`` file and adapt the IP addresses and SSH user (sample here: `inventory <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/standalone/01_inventory.ini>`__)

  .. code-block:: shell

    [all]
    node1 ansible_host=10.0.0.1 # Change it with the IP of the single server

    ...

  .. code-block:: shell

    [all:vars]
    ansible_user=root # Change it accordingly

You can check that everything is well configured using this command:

  .. code-block:: shell

    ansible all -i inventories/standalone -bv -m ping

Run these commands:

-  To download and install requirements:

  .. code-block:: shell

    ./requirements_install.sh

- To deploy:

  .. code-block:: shell

    ansible-playbook -i inventories/standalone main.yml

Single node feature
===================

By default, OpenIO does not support the installation of all its services on the same server.
The most problematic part is that a RAWX service can not be on the same server as the service.
It's a protection because:

- RAWX stores the data
- RDIR stores information about the data stored in a given RAWX

So if RAWX does not respond, its data can be reconstructed elsewhere.
If both services are on the same server, the data is lost and the informations about this data is lost too !

  .. code-block:: shell

    [root@11ce9e9fe3de ~]# openio cluster list
    +---------+-----------------+------------+---------------------------------+--------------+-------+------+-------+
    | Type    | Addr            | Service Id | Volume                          | Location     | Slots | Up   | Score |
    +---------+-----------------+------------+---------------------------------+--------------+-------+------+-------+
    | account | 172.17.0.2:6009 | n/a        | n/a                             | 11ce9e9fe3de | n/a   | True |    89 |
    | meta0   | 172.17.0.2:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | 11ce9e9fe3de | n/a   | True |    94 |
    | meta1   | 172.17.0.2:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | 11ce9e9fe3de | n/a   | True |    65 |
    | meta2   | 172.17.0.2:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | 11ce9e9fe3de | n/a   | True |    65 |
    | rawx    | 172.17.0.2:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | 11ce9e9fe3de | n/a   | True |    63 |
    | rdir    | 172.17.0.2:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | 11ce9e9fe3de | n/a   | True |    89 |
    +---------+-----------------+------------+---------------------------------+--------------+-------+------+-------+

    [root@11ce9e9fe3de ~]# openio volume assignation
    +------+-----------------+---------------+---------------+
    | Rdir | Rawx            | Rdir location | Rawx location |
    +------+-----------------+---------------+---------------+
    | n/a  | 172.17.0.2:6201 | None          | 11ce9e9fe3de  |
    +------+-----------------+---------------+---------------+

The RDIR location is 'None'. You have to force association of the RDIR with the RAWX:

.. code-block:: shell

    [root@11ce9e9fe3de ~]# openio reference create --oio-account _RDIR 172.17.0.2:6201
    +-----------------+---------+
    | Name            | Created |
    +-----------------+---------+
    | 172.17.0.2:6201 | True    |
    +-----------------+---------+
    [root@11ce9e9fe3de ~]# openio reference force --oio-account _RDIR 172.17.0.2:6201 172.17.0.2:6301 rdir
    [root@11ce9e9fe3de ~]# openio volume assignation
    +-----------------+-----------------+---------------+---------------+
    | Rdir            | Rawx            | Rdir location | Rawx location |
    +-----------------+-----------------+---------------+---------------+
    | 172.17.0.2:6301 | 172.17.0.2:6201 | 11ce9e9fe3de  | 11ce9e9fe3de  |
    +-----------------+-----------------+---------------+---------------+

Post-install Checks
===================

The node is configured to easily use the openio-cli and aws-cli.

Run this check script on one of the node involved in the cluster ``sudo /root/checks.sh``

Sample output:

::

  root@node1:~# ./checks.sh
  ## OPENIO
   Status of services.
  KEY                       STATUS      PID GROUP
  OPENIO-account-0          UP         7576 OPENIO,account,0
  OPENIO-beanstalkd-1       UP        10327 OPENIO,beanstalkd,beanstalkd-1
  OPENIO-conscience-1       UP        10518 OPENIO,conscience,conscience-1
  OPENIO-conscienceagent-1  UP        10368 OPENIO,conscienceagent,conscienceagent-1
  OPENIO-memcached-0        UP        11858 OPENIO,memcached,0
  OPENIO-meta0-1            UP        11031 OPENIO,meta0,meta0-1
  OPENIO-meta1-1            UP        11065 OPENIO,meta1,meta1-1
  OPENIO-meta2-1            UP        10614 OPENIO,meta2,meta2-1
  OPENIO-oio-blob-indexer-1 UP        10359 OPENIO,oio-blob-indexer,oio-blob-indexer-1
  OPENIO-oio-event-agent-0  UP        10498 OPENIO,oio-event-agent,oio-event-agent-0
  OPENIO-oioproxy-1         UP        10657 OPENIO,oioproxy,oioproxy-1
  OPENIO-oioswift-0         UP        14245 OPENIO,oioswift,0
  OPENIO-rawx-1             UP        10401 OPENIO,rawx,rawx-1
  OPENIO-rdir-1             UP        10515 OPENIO,rdir,rdir-1
  OPENIO-redis-1            UP        10491 OPENIO,redis,redis-1
  OPENIO-redissentinel-1    UP        10406 OPENIO,redissentinel,redissentinel-1
  --
   Display the cluster status.
  +---------+-----------------+------------+---------------------------------+----------+-------+------+-------+
  | Type    | Addr            | Service Id | Volume                          | Location | Slots | Up   | Score |
  +---------+-----------------+------------+---------------------------------+----------+-------+------+-------+
  | account | 172.17.0.2:6009 | n/a        | n/a                             | node1    | n/a   | True |    99 |
  | meta0   | 172.17.0.2:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | node1    | n/a   | True |    99 |
  | meta1   | 172.17.0.2:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | node1    | n/a   | True |    73 |
  | meta2   | 172.17.0.2:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | node1    | n/a   | True |    72 |
  | rawx    | 172.17.0.2:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | node1    | n/a   | True |    73 |
  | rdir    | 172.17.0.2:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | node1    | n/a   | True |    99 |
  +---------+-----------------+------------+---------------------------------+----------+-------+------+-------+
  --
   Upload the /etc/passwd into the bucket MY_CONTAINER of the MY_ACCOUNT project.
  +--------+------+----------------------------------+--------+
  | Name   | Size | Hash                             | Status |
  +--------+------+----------------------------------+--------+
  | passwd | 1803 | 342A63A4789FE6E4C03DB859DAE4E207 | Ok     |
  +--------+------+----------------------------------+--------+
  --
   Get some informations about your object.
  +----------------+--------------------------------------------------------------------+
  | Field          | Value                                                              |
  +----------------+--------------------------------------------------------------------+
  | account        | MY_ACCOUNT                                                         |
  | base_name      | 7B1F1716BE955DE2D677B68819836E4F75FD2424F6D22DB60F9F2BB40331A741.1 |
  | bytes_usage    | 1.803KB                                                            |
  | container      | MY_CONTAINER                                                       |
  | ctime          | 1532612697                                                         |
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
  | passwd | 1803 | 342A63A4789FE6E4C03DB859DAE4E207 | 1532612738265829 |
  +--------+------+----------------------------------+------------------+
  --
   Find the services involved for your container.
  +-----------+--------------------------------------------------------------------+
  | Field     | Value                                                              |
  +-----------+--------------------------------------------------------------------+
  | account   | MY_ACCOUNT                                                         |
  | base_name | 7B1F1716BE955DE2D677B68819836E4F75FD2424F6D22DB60F9F2BB40331A741.1 |
  | meta0     | 172.17.0.2:6001                                                    |
  | meta1     | 172.17.0.2:6111                                                    |
  | meta2     | 172.17.0.2:6121                                                    |
  | name      | MY_CONTAINER                                                       |
  | status    | Enabled                                                            |
  +-----------+--------------------------------------------------------------------+
  --
   Save the data stored in the given object to the --file destination.
  root:x:0:0:root:/root:/bin/bash
  daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
  bin:x:2:2:bin:/bin:/usr/sbin/nologin
  sys:x:3:3:sys:/dev:/usr/sbin/nologin
  sync:x:4:65534:sync:/bin:/bin/sync
  games:x:5:60:games:/usr/games:/usr/sbin/nologin
  man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
  lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
  mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
  news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
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
   Upload the /etc/passwd into the bucket mybucket.
  upload: ../etc/passwd to s3://mybucket/passwd
  --
   List your buckets.
  2018-07-26 15:45:41    1.8 KiB passwd

  Total Objects: 1
     Total Size: 1.8 KiB
  --
   Save the data stored in the given object into the file given.
  download: s3://mybucket/passwd to ../tmp/passwd.aws
  root:x:0:0:root:/root:/bin/bash
  daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
  bin:x:2:2:bin:/bin:/usr/sbin/nologin
  sys:x:3:3:sys:/dev:/usr/sbin/nologin
  sync:x:4:65534:sync:/bin:/bin/sync
  games:x:5:60:games:/usr/games:/usr/sbin/nologin
  man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
  lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
  mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
  news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
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

.. include:: manual_requirements.rst

.. include:: custom_deployment.rst
