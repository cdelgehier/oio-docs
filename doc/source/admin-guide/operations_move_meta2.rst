====================
Move a meta2 service
====================

Preparation
~~~~~~~~~~~

Find information about the container you want to move.
By running ``openio container locate <container>`` you will get the list of all meta2 service address and base name.
You can get list of container using ``openio container list``.

Launch mover
~~~~~~~~~~~~

Format name is {cid}.{seq}. The cid is the container ID and seq is the ID of sequence.

If the base name is 43839DACDD060FA939FAE2714A60640BDC5AFFDDBE8C494BDAB7AA994C3190A5.1,

the CID is 43839DACDD060FA939FAE2714A60640BDC5AFFDDBE8C494BDAB7AA994C3190A5 and the SEQ is 1.

You can launch mover by running
  .. code-block:: console

    # oio-meta2-mover <namespace> <CID> <IP:PORT source>

    43839DACDD060FA939FAE2714A60640BDC5AFFDDBE8C494BDAB7AA994C3190A5.1

This command move all sequences, but you can add the sequence ID  to only move one sequence.
The destination service is automatically selected. The command will return the bases moved.

Move to specific destination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can specifify a destination where you want to move your container.
Add the address of a service destination service on parameter, if destination isn't free or up, an error will occur.

  .. code-block:: console

    # oio-meta2-mover <namespace> <CID> <IP:PORT source> <IP:PORT destination>

With a destination not free or up the return can be:

  .. code-block:: text
		
    ERROR: source service isn't used or destination service is already used for this base
