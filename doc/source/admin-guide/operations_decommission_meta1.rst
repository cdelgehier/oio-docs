============================
Decommission a meta1 service
============================

Preparation
~~~~~~~~~~~

Find information about the service you want to decommission.
By running ``openio cluster list meta1`` you will get the list of all meta1 service address accompanied by their volume path.



Launch decommissioning
~~~~~~~~~~~~~~~~~~~~~~

Run ``openio directory decommission <IP:PORT>``, the <IP:PORT> is the the address of the meta1.


Launch decommissioning on specific bases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also decommission only some bases. You need to get base name prefix and give them on parameter.

Run ``openio container locate <container>`` to get base name. You can find container name with ``openio container list``
The prefix is the first characters of base name. The prefix size is stored on sds.conf (example: meta1_digits=4).

For example, if the base name is 43839DACDD060FA939FAE2714A60640BDC5AFFDDBE8C494BDAB7AA994C3190A5.1 and meta1_digits is equal to 4, the prefix is 4383
With meta1 <IP:PORT> equal to 127.0.0.1:6026, you can launch decommissioning
with:

  .. code-block:: console

    # openio directory decommission 127.0.0.11:6026 4383

You can give more than one base on parameter.

The ``--replicas`` option is used to change the number of replicas on meta1.

You can use ``--min-dist`` option with a big enought value to be sure that the replicas are in differents servers, racks, ...
