=====================
Scale your cluster up
=====================

Here you will learn how to scale your cluster by adding a new node.
The steps below are given for ubuntu/debian, please use the package manager belonging to your distribution.

Initialize
~~~~~~~~~~

1. Keep your system updated:

  .. code-block:: console

    # sudo apt-get update
    # sudo apt-get upgrade -y

2. Reboot to apply changes:

  .. code-block:: console

    # sudo reboot


OpenIO Packages Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On each server:

1. Configure OpenIO SDS repository

  Add the Debian Backports_ repository:

  .. code-block:: console

    # echo "deb http://httpredir.debian.org/debian $(lsb_release -c -s)-backports main contrib non-free" | sudo tee /etc/apt/sources.list.d/debian-backports.list

  Add the OpenIO SDS repository configuration:

  .. code-block:: console

    # echo "deb http://mirror.openio.io/pub/repo/openio/sds/17.04/$(lsb_release -i -s)/ $(lsb_release -c -s)/" | sudo tee /etc/apt/sources.list.d/openio-sds.list

  Install cURL if necessary:

  .. code-block:: console

    # sudo apt-get install curl -y

  Add the OpenIO archive key to verify packages signatures:

  .. code-block:: console

    # curl http://mirror.openio.io/pub/repo/openio/APT-GPG-KEY-OPENIO-0 | sudo apt-key add -

2. Install OpenIO SDS puppet module:

  .. code-block:: console

    # sudo apt-get update; sudo apt-get install puppet-module-openio-openiosds -y

.. _Backports: https://wiki.debian.org/Backports

Puppet Manifest
~~~~~~~~~~~~~~~

Now you can create a manifest file to configure your host,
here is a template to configure the services:

- Replace SERVER1, SERVER2 and SERVER3 with the corresponding IP addresses used during your first deployment.

In a file called ``/root/openio.pp``:

   .. code-block:: puppet

      class {'openiosds':}
      openiosds::namespace {'OPENIO':
        ns             => 'OPENIO',
        conscience_url => "SERVER1:6000",
        zookeeper_url  => "SERVER1:6005,SERVER2:6005,SERVER3:6005",
        oioproxy_url   => "${ipaddress}:6006",
        eventagent_url => "beanstalk://${ipaddress}:6014",
      }
      openiosds::meta2 {'meta2-0':
        ns        => 'OPENIO',
        ipaddress => $ipaddress,
      }
      openiosds::rawx {'rawx-0':
        ns        => 'OPENIO',
        ipaddress => $ipaddress,
      }
      openiosds::oioeventagent {'oio-event-agent-0':
        ns          => 'OPENIO',
        ipaddress   => $ipaddress,
      }
      openiosds::oioproxy {'oioproxy-0':
        ns        => 'OPENIO',
        ipaddress => $ipaddress,
      }
      openiosds::conscienceagent {'conscienceagent-0':
        ns  => 'OPENIO',
      }
      openiosds::beanstalkd {'beanstalkd-0':
        ns        => 'OPENIO',
        ipaddress => $ipaddress,
      }
      openiosds::rdir {'rdir-0':
        ns        => 'OPENIO',
        ipaddress => $ipaddress,
      }
      openiosds::oioblobindexer {'oio-blob-indexer-rawx-0':
        ns  => 'OPENIO',
      }

Package Installation and Service Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using puppet, we will install the packages and configure the services for your OpenIO namespace.
On each server, apply the manifest:

   .. code-block:: console

      # puppet apply --no-stringify_facts /root/openio.pp

This step may take a few minutes. Please be patient as it downloads and installs all necessary packages.
Once completed, all services should be installed and running using OpenIO GridInit.
You can verify that everything went well by performing ``gridinit_cmd status`` on every node.

    .. code-block:: console

       KEY                           STATUS      PID GROUP
       NAMESPACE-servicetype-idx     UP          pid NAMESPACE,service,servicetype-idx
       ...

Unlock scores to make new services eligible
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unlock all the new services in the namespace:

   .. code-block:: console

      # openio --oio-ns=OPENIO cluster unlockall

After unlocking, your new services should take some load!

Be sure that every score is greater than 0 using `openio cluster list`:

   .. code-block:: console

      # openio --oio-ns OPENIO cluster list
