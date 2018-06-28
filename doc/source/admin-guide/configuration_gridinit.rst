===========================
Configure a gridinit daemon
===========================

.. contents::
   :local:
   :depth: 2

The present page describes the configuration of gridinit in version
{{GRIDINIT_BRANCHNAME}}. `gridinit` is open source, you can find the sources
at {{GRIDINIT_REPOSITORY}}.

`gridinit` is not affected by the general configuration explained at
":ref:`ref-admin-guide`".

Command line options
++++++++++++++++++++

We hope the help section is enough to explain the behavior.

.. code-block:: console

   $ gridinit -h

   Usage: gridinit [OPTIONS] ... CONFIG_PATH
    with OPTIONS:
       -d       : Detaches then daemonizes the gridinit
       -h       : displays this help section
       -g GROUP : limits the services loading to those belonging to
                  the specified group. This option can be repeated.
       -q       : quiet mode, suppress non-error output
       -v       : verbose output mode.
       -s ID    : enable logs using syslog with the given ID.



Section "Default"
+++++++++++++++++

env.KEY
-------

gid
---

include
-------

inherit_env
-----------

limit.core_size
---------------

limit.stack_size
----------------

limit.max_files
---------------

listen
------

pidfile
-------

uid
---

working_dir
-----------

Sections "service.*"
++++++++++++++++++++

command
-------

enabled
-------

group
-----

on_die
------

start_at_boot
-------------

Sample configuration
++++++++++++++++++++

.. code-block:: ini

   [Default]
   listen=/path/to/gridinit.sock
   pidfile=/path/to/gridinit.pid
   uid=1000
   gid=1000
   working_dir=/tmp
   inherit_env=1
   env.PATH=/usr/local/bin:/usr/local/sbin
   env.LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64

   limit.core_size=-1
   limit.max_files=2048
   # In MiB
   limit.stack_size=256

   include=/etc/oio/sds.conf.d/*-gridinit.conf

   [service.service-1]
   group=OPENIO,localhost,srvtype,10.0.0.1
   on_die=cry
   enabled=true
   start_at_boot=true
   command=/bin/sleep 3600

