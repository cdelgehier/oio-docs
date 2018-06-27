=========================
Troubleshoot a deployment
=========================

.. contents::
   :depth: 1
   :local:

You find below, the results of checks when we deployed OpenIO SDS on Cent0S 7
and Ubuntu 16.4 cluster with the last release pull by Cédric. The overarching
aim of to check compatibility between old playbook and last roles.

Technical Architecture
++++++++++++++++++++++

Each platform will be composed of the following servers:

  -  3 x nodes with CentOS 7 (1CPU, 1GB RAM, 1Gb/s)
  -  3 x nodes with Ubuntu 16.4 (1CPU, 1GB RAM, 1Gb/s)
  -  1 x admin node witch Cent0S 7 (1CPU, 1GB RAM)


Prepare yourself with the survival kit
++++++++++++++++++++++++++++++++++++++

On first step, only one cluster OpenIO SDS playbook are check and the new role
`install_basic_needs`. After discussion with Cédric, we decide that the
`install_basic_needs` role was expected to be deployed on first.

After execute this playbook with this command-line:

.. code-block:: console

   # ansible-playbook install_basic_needs.yml

This playbook performs repositories, ntp, and survivalkit roles.


No package matching python-pip
++++++++++++++++++++++++++++++

Global Task Status for CentOS Troubleshooting:

::

  failed: [192.168.1.105] (item=python-pip) => {"changed": false, "msg": "No package matching 'python-pip' found available, installed or updated", "pkg": "python-pip", "rc": 126, "results": ["No package matching 'python-pip' found available, installed or updated"]}
  failed: [192.168.1.106] (item=htop) => {"changed": false, "msg": "No package matching 'htop' found available, installed or updated", "pkg": "htop", "rc": 126, "results": ["No package matching 'htop' found available, installed or updated"]}
  failed: [192.168.1.103] (item=iftop) => {"changed": false, "msg": "No package matching 'iftop' found available, installed or updated", "pkg": "iftop", "rc": 126, "results": ["No package matching 'iftop' found available, installed or updated »]}


Cause: These packages are on `epel-repo` but it’s not installed on each nodes

Resolving the problem:

- Add `epel-release` to the top of the packages list because `iftop`, `atop`
  and `python2-pip` packages are on this repository.
- Patch(s) to add for resolve the above cases.


::

  --- /root/customer-centos/ansible/deployment/roles/survivalkit/vars/RedHat.yml.bak 2018-06-26 14:19:08.739985248 +0000
  +++ /root/customer-centos/ansible/deployment/roles/survivalkit/vars/RedHat.yml 2018-06-26 14:19:51.800607516 +0000
  @@ -2,6 +2,7 @@
  # Distribution-specific variables for RHEL, CentOS, ... ---
  survivalkit_packages:
  + - epel-release - atop
  - bash-completion - bind-utils


Failure talking to yum
++++++++++++++++++++++

::

  failed: [192.168.1.106] (item=nc) => {"changed": false, "msg": "Failure talking to yum: failure: repodata/ repomd.xml from centos-qemu-ev: [Errno 256] No more mirrors to try.\nhttp://mirror.centos.org/altarch/7/ virt/x86_64/kvm-common/repodata/repomd.xml: [Errno 14] HTTP Error 404 - Not Found", "pkg": "nc"} failed: [192.168.1.103] (item=nc) => {"changed": false, "msg": "Failure talking to yum: failure: repodata/ repomd.xml from centos-qemu-ev: [Errno 256] No more mirrors to try.\nhttp://mirror.centos.org/altarch/7/ virt/x86_64/kvm-common/repodata/repomd.xml: [Errno 14] HTTP Error 404 - Not Found", "pkg": "nc"}


Cause: One of the configured repositories failed (Cent0S-7 - QEMU EV)

Resolving the problem:
The following workaround explain on patch is needed for resolved these errors.

- Patch(s) to add for resolve the above cases.
- One of the configured repositories failed (CentOS-7 - QEMU EV), and yum
  doesn't have enough cached data to continue. At this point the only
  safe thing yum can do is fail. There are a few ways to work "fix" this:

   - Contact the upstream for the repository and get them to fix the problem.
   - Reconfigure the baseurl/etc. for the repository, to point to a working
     upstream. This is most often useful if you are using a newer distribution
     release than is supported by the repository (and the packages for the
     previous distribution release still work).
   - Run the command with the repository temporarily disabled
     yum --disablerepo=centos-qemu-ev ...
   - Disable the repository permanently, so yum won't use it by default. Yum
     will then just ignore the repository until you permanently enable it again
     or use --enablerepo for temporary usage:
     yum-config-manager --disable centos-qemu-ev
     or
     subscription-manager repos --disable=centos-qemu-ev
   - Configure the failing repository to be skipped, if it is unavailable.
     Note that yum will try to contact the repo. when it runs most commands,
     so will have to try and fail each time (and thus. yum will be be much
     slower). If it is a very temporary problem though, this is often a nice
     compromise:

.. code-block:: console

   $ yum-config-manager --save --setopt=centos-qemu-ev.skip_if_unavailable=true


nc: command not found
++++++++++++++++++++++

install should be done before.
Wait for Zookeeper to be online.

::

  TASK (failed: [10.0.0.14] (item=10.0.0.14) => {"attempts": 10, "changed": true, "cmd": "echo ruok | nc 10.0.0.14 6005", "delta": "0:00:00.004663", "end": "2018-06-11 15:26:20.575484", "item": "10.0.0.14", "msg": "non-zero return code", "rc": 127, "start": "2018-06-11 15:26:20.570821", "stderr": "/bin/sh: nc : commande introuvable", "stderr_lines": ["/bin/sh: nc : commande introuvable"], "stdout": "", "stdout_lines": []})

Cause: Netcat is not installed

Resolving the problem:

- Install should be done before
- Wait for Zookeeper to be online
- Patch(s) to add for resolve the above cases.


TASK [Gathering Facts]
++++++++++++++++++++++

::

  FAILED! => {"changed": false, "module_stderr": "Shared connection to xx.xx.xx.xx closed.\r\n", "module_stdout": "/bin/sh: 1: /usr/bin/python: not found\r\n", "msg": "MODULE FAILURE", "rc": 0}

Cause: Python is not installed on remote node.

Resolving the problem:

- Install python on each nodes manually, with the following command line: `# apt-get -y install python`
- Patch(s) to add for resolve the above cases.


TASK [survivalkit: Install packages]
+++++++++++++++++++++++++++++++++++++

::

  failed: [xx.xx.xx.xx] (item=tdpdump) => {"changed": false, "msg": "No package matching 'tdpdump' is available", "pkg": "tdpdump"}


Cause: Syntax error!

Resolving the problem:

- Replace tdpdump by tcpdump.
- Patch(s) to add for resolve the above cases.

::

  --- roles/survivalkit/vars/Debian.yml.back
  +++ roles/survivalkit/vars/Debian.yml @@ -25,7 +25,7 @@
  - strace - sysstat - tar
  - - tdpdump + - tcpdump
  2018-06-26 14:06:57.811271968 +0000 2018-06-26 14:07:19.791084043 +0000
  - telnet - tmux - vim
  ————————

TASK [openio-sds: OpenIO SDS: Set sysctl parameters]
+++++++++++++++++++++++++++++++++++++++++++++++++++++

Buffer and other variables, are not set automatically by OS, it is possible
that we have tcp buffer errors.

Cause: OpenIO set variables

Resolving the problem:

- Kernel should be set variables.
- Patch(s) to add for resolve the above cases.


TASK [openio-sds: Install OpenIO puppet module]
++++++++++++++++++++++++++++++++++++++++++++++++

::

  fatal: [192.168.1.138]: FAILED! => {"changed": false, "msg": "No package matching 'puppet-module-openio- openiosds' is available »}


Cause: Repositories are not deployed.

Resolving the problem:

- Use the playbook `install_basic_needs.yml`, and define `openio_sds_version`
- Patch(s) to add for resolve the above cases.


TASK [repositories: Configure repositories for Ubuntu xenial]
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

::

  fatal: [192.168.1.116]: FAILED! => {"msg": "{u'sds': {u'release': u'{{ openio_sds_release }}'}}: 'openio_sds_release' is undefined"}


Cause: The `openio_sds_release` is not set correctly. E.g. it might happen when
we deploy a `{RELEASE}` instead of `{RELEASE} sys` release)

Resolving the problem:

- Remove the wrong repository,
- Patch(s) to add for resolve the above cases.
- Add a check release (wget or curl), before deployed the repository
  configuration on each nodes.


TASK [survivalkit: Include Ubuntu variables]
+++++++++++++++++++++++++++++++++++++++++++++

::

  fatal: [192.168.1.116]: FAILED! => {"msg": "The conditional check 'install_survival_kit' failed. The error was: error while evaluating conditional (install_survival_kit): 'install_survival_kit' is undefined\n\nThe error appears to have been in '/root/customer-ubuntu/ansible/deployment/roles/survivalkit/tasks/main.yml': line 3, column 3, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n---\n- name: \"Include {{ ansible_distribution }} variables\"\n ^ here\nWe could be wrong, but this one looks like it might be an issue with\nmissing quotes. Always quote template expression brackets when they\nstart a value. For instance:\n\n with_items:\n - {{ foo }}\n\nShould be written as:\n\n with_items: \n - \"{{ foo }}\ »\n"}


Cause: Wrong syntax!

Resolving the problem:

- As reminder, this list of installed packages is slated to disappear, so that
  we  disable it.
- Patch(s) to add for resolve the above cases.

