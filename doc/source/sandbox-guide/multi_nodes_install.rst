.. title:: Deploy a multi-node Swift/S3 on premise object storage backend

.. _ref-install-guide:

========================
Multi Nodes Installation
========================

.. contents::
   :backlinks: none
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
-  Ubuntu 18.04 (Server)

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

    git clone https://github.com/open-io/ansible-playbook-openio-deployment.git --branch 18.10 oiosds && cd oiosds/products/sds

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

- Edit the ``inventory.ini`` file and adapt the IP addresses and SSH user (sample here: `inventory <https://github.com/open-io/ansible-playbook-openio-deployment/blob/18.10/products/sds/inventory.ini>`__).

  .. code-block:: shell

    [all]
    node1 ansible_host=10.0.0.1 # Change it with the IP of the first server
    node2 ansible_host=10.0.0.2 # Change it with the IP of the second server
    node3 ansible_host=10.0.0.3 # Change it with the IP of the third server
    ...

  .. code-block:: shell

    [all:vars]
    ansible_user=root # Change it accordingly

Ensure you have a ssh access to your nodes

  .. code-block:: shell

    # generate a ssh key
    $> ssh-keygen

    # copy the key on all nodes
    $> for node in <name-of-remote-server1> <name-of-remote-server2> <name-of-remote-server3>; do ssh-copy-id $node; done

    # start a ssh-agent
    $> eval "$(ssh-agent -s)"

    # test connection
    $> ssh <name-of-remote-server1>

You can check that everything is configured correctly using this command:

  .. code-block:: shell

    # RedHat
    ansible all -i inventory.ini -bv -m ping

    # Ubuntu
    ansible all -i inventory.ini -bv -m ping -e 'ansible_python_interpreter=/usr/bin/python3'


Run these commands:

-  To download and install requirements:

  .. code-block:: shell

    ./requirements_install.sh

- To deploy and initialize the cluster:

  .. code-block:: shell

    ./deploy_and_bootstrap.sh

Post-installation Checks
========================

All the nodes are configured to use openio-cli and aws-cli.

Run this check script on one of the nodes in the cluster ``sudo /root/checks.sh``.

Sample output:

::

  root@sds-cde-1:~# ./checks.sh
  ## OPENIO
   Status of services.
  KEY                         STATUS      PID GROUP
  OPENIO-account-0            UP        23724 OPENIO,account,0
  OPENIO-beanstalkd-0         UP        23725 OPENIO,beanstalkd,0
  OPENIO-conscienceagent-0    UP        23721 OPENIO,conscienceagent,0
  OPENIO-memcached-0          UP        23720 OPENIO,memcached,0
  OPENIO-meta0-0              UP        23772 OPENIO,meta0,0
  OPENIO-meta1-0              UP        23771 OPENIO,meta1,0
  OPENIO-meta2-0              UP        23770 OPENIO,meta2,0
  OPENIO-oio-blob-indexer-0   UP        23723 OPENIO,oio-blob-indexer,0
  OPENIO-oio-blob-rebuilder-0 UP        23722 OPENIO,oio-blob-rebuilder,0
  OPENIO-oio-event-agent-0    UP        23767 OPENIO,oio-event-agent,0
  OPENIO-oioproxy-0           UP        23773 OPENIO,oioproxy,0
  OPENIO-oioswift-0           UP        23719 OPENIO,oioswift,0
  OPENIO-rawx-0               UP        23769 OPENIO,rawx,0
  OPENIO-rdir-0               UP        23768 OPENIO,rdir,0
  OPENIO-redis-0              UP        23727 OPENIO,redis,0
  OPENIO-redissentinel-0      UP        23726 OPENIO,redissentinel,0
  OPENIO-zookeeper-0          UP        23728 OPENIO,zookeeper,0
  --
   Display the cluster status.
  +---------+----------------+------------+---------------------------------+-------------+-------+------+-------+
  | Type    | Addr           | Service Id | Volume                          | Location    | Slots | Up   | Score |
  +---------+----------------+------------+---------------------------------+-------------+-------+------+-------+
  | account | 10.0.1.11:6009 | n/a        | n/a                             | sds-cde-3.0 | n/a   | True |   100 |
  | account | 10.0.1.13:6009 | n/a        | n/a                             | sds-cde-2.0 | n/a   | True |    99 |
  | account | 10.0.1.14:6009 | n/a        | n/a                             | sds-cde-1.0 | n/a   | True |    70 |
  | meta0   | 10.0.1.11:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-0 | sds-cde-3.0 | n/a   | True |   100 |
  | meta0   | 10.0.1.13:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-0 | sds-cde-2.0 | n/a   | True |    99 |
  | meta0   | 10.0.1.14:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-0 | sds-cde-1.0 | n/a   | True |    90 |
  | meta1   | 10.0.1.11:6110 | n/a        | /var/lib/oio/sds/OPENIO/meta1-0 | sds-cde-3.0 | n/a   | True |    93 |
  | meta1   | 10.0.1.13:6110 | n/a        | /var/lib/oio/sds/OPENIO/meta1-0 | sds-cde-2.0 | n/a   | True |    93 |
  | meta1   | 10.0.1.14:6110 | n/a        | /var/lib/oio/sds/OPENIO/meta1-0 | sds-cde-1.0 | n/a   | True |    92 |
  | meta2   | 10.0.1.11:6120 | n/a        | /var/lib/oio/sds/OPENIO/meta2-0 | sds-cde-3.0 | n/a   | True |    93 |
  | meta2   | 10.0.1.13:6120 | n/a        | /var/lib/oio/sds/OPENIO/meta2-0 | sds-cde-2.0 | n/a   | True |    93 |
  | meta2   | 10.0.1.14:6120 | n/a        | /var/lib/oio/sds/OPENIO/meta2-0 | sds-cde-1.0 | n/a   | True |    92 |
  | rawx    | 10.0.1.11:6200 | n/a        | /var/lib/oio/sds/OPENIO/rawx-0  | sds-cde-3.0 | n/a   | True |    93 |
  | rawx    | 10.0.1.13:6200 | n/a        | /var/lib/oio/sds/OPENIO/rawx-0  | sds-cde-2.0 | n/a   | True |    93 |
  | rawx    | 10.0.1.14:6200 | n/a        | /var/lib/oio/sds/OPENIO/rawx-0  | sds-cde-1.0 | n/a   | True |    93 |
  | rdir    | 10.0.1.11:6300 | n/a        | /var/lib/oio/sds/OPENIO/rdir-0  | sds-cde-3.0 | n/a   | True |   100 |
  | rdir    | 10.0.1.13:6300 | n/a        | /var/lib/oio/sds/OPENIO/rdir-0  | sds-cde-2.0 | n/a   | True |    99 |
  | rdir    | 10.0.1.14:6300 | n/a        | /var/lib/oio/sds/OPENIO/rdir-0  | sds-cde-1.0 | n/a   | True |    70 |
  +---------+----------------+------------+---------------------------------+-------------+-------+------+-------+
  --
   Upload the /etc/passwd into the bucket MY_CONTAINER of the MY_ACCOUNT project.
  +--------+------+----------------------------------+--------+
  | Name   | Size | Hash                             | Status |
  +--------+------+----------------------------------+--------+
  | passwd | 1996 | 420C3FC20631F95B6EED50E7423295F6 | Ok     |
  +--------+------+----------------------------------+--------+
  --
   Get some informations about your object.
  +----------------+--------------------------------------------------------------------+
  | Field          | Value                                                              |
  +----------------+--------------------------------------------------------------------+
  | account        | MY_ACCOUNT                                                         |
  | base_name      | 7B1F1716BE955DE2D677B68819836E4F75FD2424F6D22DB60F9F2BB40331A741.1 |
  | bytes_usage    | 1.996KB                                                            |
  | container      | MY_CONTAINER                                                       |
  | ctime          | 1540562156                                                         |
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
  | passwd | 1996 | 420C3FC20631F95B6EED50E7423295F6 | 1540562156802496 |
  +--------+------+----------------------------------+------------------+
  --
   Find the services involved for your container.
  +-----------------+--------------------------------------------------------------------+
  | Field           | Value                                                              |
  +-----------------+--------------------------------------------------------------------+
  | account         | MY_ACCOUNT                                                         |
  | base_name       | 7B1F1716BE955DE2D677B68819836E4F75FD2424F6D22DB60F9F2BB40331A741.1 |
  | meta0           | 10.0.1.11:6001, 10.0.1.13:6001, 10.0.1.14:6001                     |
  | meta1           | 10.0.1.11:6110, 10.0.1.13:6110, 10.0.1.14:6110                     |
  | meta2           | 10.0.1.11:6120, 10.0.1.14:6120, 10.0.1.13:6120                     |
  | meta2.sys.peers | 10.0.1.11:6120, 10.0.1.13:6120, 10.0.1.14:6120                     |
  | name            | MY_CONTAINER                                                       |
  | status          | Enabled                                                            |
  +-----------------+--------------------------------------------------------------------+
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
   Show the account informations.
  +------------+------------+
  | Field      | Value      |
  +------------+------------+
  | account    | MY_ACCOUNT |
  | bytes      | 1.996KB    |
  | containers | 1          |
  | ctime      | 1540497830 |
  | metadata   | {}         |
  | objects    | 1          |
  +------------+------------+
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
  2018-10-26 13:56:00    1.9 KiB passwd

  Total Objects: 1
     Total Size: 1.9 KiB
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
  --
  Done !

  ++++
   AWS S3 summary:
    endpoint: http://10.0.1.14:6007
    region: us-east-1
    access key: demo:demo
    secret key: DEMO_PASS
    ssl: false
    signature_version: s3v4
    path style: true


.. include:: manual_requirements.rst

.. include:: custom_deployment.rst
