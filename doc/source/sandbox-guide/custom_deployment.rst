Custom your deployment
======================

Manage NTP configuration
------------------------

You can set the time settings in the `all.yml <https://github.com/open-io/ansible-playbook-openio-deployment/tree/master/products/sds/inventories/n-nodes/group_vars/all.yml>`__ file.
By default, the deployment dont change your timezone but enable the NTP service and set 4 NTP servers

.. code-block:: yaml
   :caption: all.yml

   ---
   # NTP
   ntp_enabled: true
   ntp_manage_config: true
   ntp_manage_timezone: false
   ntp_timezone: "Etc/UTC"
   ntp_area: ""
   ntp_servers:
     - "0{{ ntp_area }}.pool.ntp.org iburst"
     - "1{{ ntp_area }}.pool.ntp.org iburst"
     - "2{{ ntp_area }}.pool.ntp.org iburst"
     - "3{{ ntp_area }}.pool.ntp.org iburst"
   ntp_restrict:
     - "127.0.0.1"
     - "::1"
   ...

If needed, you can set your own settings:

.. code-block:: yaml
   :caption: all.yml

   ---
   # NTP
   ntp_enabled: true
   ntp_manage_config: true
   ntp_manage_timezone: true
   ntp_timezone: "Europe/Paris"
   ntp_area: ".fr"
   ntp_servers:
     - "0{{ ntp_area }}.pool.ntp.org iburst"
     - "1{{ ntp_area }}.pool.ntp.org iburst"
     - "2{{ ntp_area }}.pool.ntp.org iburst"
     - "3{{ ntp_area }}.pool.ntp.org iburst"
   ntp_restrict:
     - "127.0.0.1"
     - "::1"
   ...

Manage storage volume
---------------------

You can customize all storage device by node in the `host_vars <https://github.com/open-io/ansible-playbook-openio-deployment/tree/master/products/sds/inventories/n-nodes/host_vars>`__ folder.
In this example, the node have 2 mounted volumes to store the data and 1 to store the metadata:

.. code-block:: yaml
   :caption: node1.yml

   ---
   openio_data_mounts:
     - { mountpoint: "/mnt/sda1" }
     - { mountpoint: "/mnt/sda2" }
   openio_metadata_mounts:
     - { mountpoint: "/mnt/ssd1" }
   ...

Manage the ssh connection
-------------------------

If one of your node haven't the same ssh user, you can define a particular ssh user (or key) used for the deployment of this node .

.. code-block:: yaml
   :caption: node1.yml

   ---
   ansible_user: my_user
   ansible_ssh_private_key_file: /home/john/.ssh/id_rsa
   #ansible_port: 2222
   #ansible_python_interpreter: /usr/local/bin/python
   ...

Manage the data network interface used
--------------------------------------

Globally, the interface used for data is defined by ``openio_bind_interface`` in the `openio.yml <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/n-nodes/group_vars/openio.yml>`__. You can define a specific interface for one node in its ``host_vars`` file.

.. code-block:: yaml
   :caption: node1.yml

   ---
   openio_bind_interface: eth2
   ...

Manage the data network interface used
--------------------------------------

If you prefer define each IP address to use instead of a global interface, you can set it in the ``host_vars`` files.

.. code-block:: yaml
  :caption: node1.yml

  ---
  openio_bind_address: 172.16.20.1
  ...

Manage S3 authentification
--------------------------

Set ``name``, ``password`` and ``role`` in the `openio.yml <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/n-nodes/group_vars/openio.yml>`__.

.. code-block:: yaml
  :caption: openio.yml

  ---
  # S3 users
  openio_oioswift_users:
    - name: "demo:demo"
      password: "DEMO_PASS"
      roles:
        - admin
    - name: "test:tester"
      password: "testing"
      roles:
        - admin
        - reseller_admin
  ...

Docker nodes
------------

If you don't have physical nodes to test our solution, you can spawn some *docker* containers with the script provided

.. code-block:: shell
  :caption: example

  $ ./spawn_my_lab.sh 3
  Replace with the following in the file named "01_inventory.ini"
  [all]
  node1 ansible_host=11ce9e9fecde ansible_user=root ansible_connection=docker
  node2 ansible_host=12cd8e2fxdel ansible_user=root ansible_connection=docker
  node3 ansible_host=13fe6e4ehier ansible_user=root ansible_connection=docker

  Change the variables in group_vars/openio.yml and adapt to your host capacity
