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

-  root privileges are required (using sudo)

  .. code-block:: shell

    # /etc/sudoers
    john    ALL=(ALL)    NOPASSWD: ALL

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

You only need to do this setup on the node (or your laptop) that will install the cluster

-  Install Ansible (versions 2.4 or 2.5) (`official guide <https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html>`__)
-  Install git for download requirements
-  Clone the OpenIO ansible playbook deployment repository (or download it with wget and unzip)
-  Install ``python-netaddr``

  .. code-block:: shell

    # RedHat
    sudo yum install git python-netaddr -y

  .. code-block:: shell

    # Ubuntu
    sudo apt install git python-netaddr -y

  .. code-block:: shell

    # Both
    git clone https://github.com/open-io/ansible-playbook-openio-deployment.git oiosds

Architecture
============

This playbook will deploy a single node like below

  .. code-block:: shell

    +-----------------+
    |     KEYSTONE    |
    |                 |
    +-----------------+
    |     DATABASE    |
    +-----------------+
    |     OIOSWIFT    |
    |                 |
    +-----------------+
    |      OPENIO     |
    |       SDS       |
    +-----------------+




Installation
============

If you don't have physical node to test our solution, you can spawn one *docker* container with the script provided

  .. code-block:: shell

    $ ./spawn_my_lab.sh 1
    Replace with the following in the file named "01_inventory.ini"
    [all]
    node1 ansible_host=11ce9e9fe3de ansible_user=root ansible_connection=docker

    Change the variables in group_vars/openio.yml and adapt to your host capacity

After filling the inventory:

- `inventory <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/standalone/01_inventory.ini>`__ (Adapt IP address and user ssh)
- `OpenIO configuration <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/standalone/group_vars/openio.yml>`__

You can check your customization like this:

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

Log into the node and run the after install check script ``/root/checks.sh``


Sample output:


::

  [root@11ce9e9fe3de ~]# ./checks.sh
  ## OPENIO
   Status of services.
  KEY                       STATUS      PID GROUP
  OPENIO-account-0          UP        17493 OPENIO,account,0
  OPENIO-beanstalkd-1       UP        17489 OPENIO,beanstalkd,beanstalkd-1
  OPENIO-conscience-1       UP        17480 OPENIO,conscience,conscience-1
  OPENIO-conscienceagent-1  UP        17491 OPENIO,conscienceagent,conscienceagent-1
  OPENIO-ecd-0              UP        17479 OPENIO,ecd,0
  OPENIO-keystone-0.0       UP        17477 OPENIO,keystone,0,keystone-wsgi-public
  OPENIO-keystone-0.1       UP        17476 OPENIO,keystone,0,keystone-wsgi-admin
  OPENIO-memcached-0        UP        17478 OPENIO,memcached,0
  OPENIO-meta0-1            UP        17488 OPENIO,meta0,meta0-1
  OPENIO-meta1-1            UP        17487 OPENIO,meta1,meta1-1
  OPENIO-meta2-1            UP        17486 OPENIO,meta2,meta2-1
  OPENIO-oio-blob-indexer-1 UP        17481 OPENIO,oio-blob-indexer,oio-blob-indexer-1
  OPENIO-oio-event-agent-0  UP        17490 OPENIO,oio-event-agent,oio-event-agent-0
  OPENIO-oioproxy-1         UP        17492 OPENIO,oioproxy,oioproxy-1
  OPENIO-oioswift-0         UP        17475 OPENIO,oioswift,0
  OPENIO-rawx-1             UP        17483 OPENIO,rawx,rawx-1
  OPENIO-rdir-1             UP        17482 OPENIO,rdir,rdir-1
  OPENIO-redis-1            UP        17484 OPENIO,redis,redis-1
  OPENIO-redissentinel-1    UP        17485 OPENIO,redissentinel,redissentinel-1
  OPENIO-zookeeper-0        UP        17494 OPENIO,zookeeper,0
  --
   Display the cluster status.
  +---------+-----------------+------------+---------------------------------+--------------+-------+------+-------+
  | Type    | Addr            | Service Id | Volume                          | Location     | Slots | Up   | Score |
  +---------+-----------------+------------+---------------------------------+--------------+-------+------+-------+
  | account | 172.17.0.2:6009 | n/a        | n/a                             | 11ce9e9fe3de | n/a   | True |    53 |
  | meta0   | 172.17.0.2:6001 | n/a        | /var/lib/oio/sds/OPENIO/meta0-1 | 11ce9e9fe3de | n/a   | True |    74 |
  | meta1   | 172.17.0.2:6111 | n/a        | /var/lib/oio/sds/OPENIO/meta1-1 | 11ce9e9fe3de | n/a   | True |    56 |
  | meta2   | 172.17.0.2:6121 | n/a        | /var/lib/oio/sds/OPENIO/meta2-1 | 11ce9e9fe3de | n/a   | True |    56 |
  | rawx    | 172.17.0.2:6201 | n/a        | /var/lib/oio/sds/OPENIO/rawx-1  | 11ce9e9fe3de | n/a   | True |    56 |
  | rdir    | 172.17.0.2:6301 | n/a        | /var/lib/oio/sds/OPENIO/rdir-1  | 11ce9e9fe3de | n/a   | True |    53 |
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
  | ctime          | 1530658716                                                         |
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
  | passwd | 1273 | 217F67C9C35A6C84B58B852DBF0C4BA2 | 1530658716068342 |
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
  2018-07-04 00:58:41    1.2 KiB passwd

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
