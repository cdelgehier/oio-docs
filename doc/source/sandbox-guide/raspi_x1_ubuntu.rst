.. _ref-install-raspberry-pi-standalone:

====================================
SDS on a Raspberry PI
====================================

This guide explains how to install OpenIO SDS in standalone mode on a Raspberry Pi 3 Model B running Ubuntu Xenial 64 bit.

Requirements
~~~~~~~~~~~~

- Raspberry Pi 3 Model B
- SD Card with at least 2GB free space
- Host Machine running Linux
- Basic Ethernet cable setup with a DHCP server (to provide an IP address for the Raspberry PI)

Prepare the SD Card
~~~~~~~~~~~~~~~~~~~

Download an OpenIO SDS image to your host machine.

   .. code-block:: shell

    $ wget {{RPI_IMAGE}} -O openio.img.zip
    $ unzip openio.img.zip

Insert the SD card into your host machine and write the image onto it.

   .. code-block:: shell

    # [DEVICE] refers to the device of your SD card, most probably it will be /dev/mmcblk0
    # You can check currently present devices using lsblk
    $ sudo dd if=$(pwd)/openio.img of=[DEVICE] status=progress bs=4M


Boot the Raspberry Pi
~~~~~~~~~~~~~~~~~~~~~

Remove the SD card from the host machine and insert it into the Raspberry Pi. Plug in the Ethernet cable. You might also plug in an HDMI cable, although this isn’t necessary. Finally, plug in the power cable and let the Raspberry Pi boot.

Let the first-time setup complete. The Raspberry Pi will have to reboot once in order to resize its partition to the size of the SD card. This should take a few minutes.


Test OpenIO
~~~~~~~~~~~

You can now use OpenIO via any of the 3 options listed below. `RPI_IP` is the IP address given to your Raspberry PI by your
DHCP server.

- **Using the OpenIO CLI**


Login into your Raspberry Pi (login: root; password: root) via SSH and create an object:

   .. code-block:: shell

    $ ssh root@[RPI_IP]

    $ openio object create --oio-ns OPENIO --oio-account testacc testcont /etc/magic
    +-------+------+----------------------------------+--------+
    | Name  | Size | Hash                             | Status |
    +-------+------+----------------------------------+--------+
    | magic |  111 | 272913026300E7AE9B5E2D51F138E674 | Ok     |
    +-------+------+----------------------------------+--------+

- **Using Swift**


Install python-swiftclient on your host machine and upload a file:

   .. code-block:: shell

    $ apt -y install python-swiftclient

    $ swift -A http://[RPI_IP]:6007/auth/v1.0/ -U demo:demo -K DEMO_PASS upload container1 /etc/hostname
    etc/hostname

- **Using S3**


For example, using awsclis:

   .. code-block:: shell

    $ apt -y install awscli
    $ mkdir -p ~/.aws
    $ cat << EOF > ~/.aws/credentials
    [default]
    aws_access_key_id=demo:demo
    aws_secret_access_key=DEMO_PASS
    s3 =
        signature_version = s3
    EOF
    $ aws --endpoint-url http://[RPI_IP]:6007 --no-verify-ssl s3 cp /proc/cpuinfo s3://mycontainer/
    upload: ../../proc/cpuinfo to s3://mycontainer/cpuinfo

Known limitations
~~~~~~~~~~~~~~~~~

- One major limitation of the current setup is that the Raspberry Pi must have a fixed IP address. If you write the image onto the SD card again, and start over with a new IP address, this will result in data loss.

- Another limitation is that the current setup is not designed to be scalable, and is provided as is, as a standalone node, meant solely for testing purposes. Please refer to our other guides to learn how to set up a scalable OpenIO cluster.
