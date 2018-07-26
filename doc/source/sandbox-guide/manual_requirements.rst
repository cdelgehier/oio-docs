Manual requirements
===================

By default, the deployment aims to be as simple as possible.
Set ``openio_manage_os_requirement`` to ``false`` in the file `all.yml <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/n-nodes/group_vars/all.yml>`__ if you wish to manually manage your requirements.

SELinux and AppArmor
--------------------

`SELinux <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/sect-security-enhanced_linux-working_with_selinux-changing_selinux_modes>`__ or `AppArmor <https://help.ubuntu.com/lts/serverguide/apparmor.html.en>`__ have to be disabled:

  .. code-block:: shell

    # RedHat
    sudo sed -i -e 's@^SELINUX=enforcing$@SELINUX=disabled@g' /etc/selinux/config
    sudo setenforce 0
    sudo systemctl disable selinux.service

  .. code-block:: shell

    # Ubuntu
    sudo service apparmor stop
    sudo apparmor teardown
    sudo update-rc.d -f apparmor remove

Firewall
--------

Firewall have to be disabled:

  .. code-block:: shell

    # RedHat
    sudo systemctl stop firewalld.service
    sudo systemctl disable firewalld.service

  .. code-block:: shell

    # Ubuntu
    sudo sudo ufw disable
    sudo systemctl disable ufw.service

Proxy
-----

Set your variables environment in the file `all.yml <https://github.com/open-io/ansible-playbook-openio-deployment/blob/master/products/sds/inventories/n-nodes/group_vars/all.yml>`__.

  .. code-block:: shell

    openio_environment:
      http_proxy: http://proxy.example.com:8080
      https_proxy: http://proxy.bos.example.com:8080
