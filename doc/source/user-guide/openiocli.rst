.. _ref-user-guide:

===================
OpenIO End-User CLI
===================

Using the command line
======================

To list available commands run ``openio help``:

   .. code-block:: console

    # openio help

    usage: openio [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]
                  [--oio-ns <namespace>] [--oio-account <account>]
                  [--oio-proxyd-url <proxyd url>] [--admin]

    Command-line interface to the OpenIO APIs

    optional arguments:
      --version             show program's version number and exit
      -v, --verbose         Increase verbosity of output. Can be repeated.
      -q, --quiet           Suppress output except warnings and errors.
      --log-file LOG_FILE   Specify a file to log output. Disabled by default.
      -h, --help            Show help message and exit.
      --debug               Show tracebacks on errors.
      --oio-ns <namespace>  Namespace name (Env: OIO_NS)
      --oio-account <account>
                            Account name (Env: OIO_ACCOUNT)
      --oio-proxyd-url <proxyd url>
                            Proxyd URL (Env: OIO_PROXYD_URL)
      --admin               passing commands into admin mode

    Commands:
    [...]

Help on specific commands
-------------------------

To get help on any command, use the ``help`` command.

   .. code-block:: console

    # openio help container create

    usage: openio container create [-h] [-f {csv,html,json,table,value,yaml}]
                   [-c COLUMN] [--max-width <integer>]
                   [--quote {all,minimal,none,nonnumeric}]
                   <container-name> [<container-name> ...]

    Create container

    positional arguments:
    <container-name>      New container name(s)
    [...]


Get started
-----------

To use the CLI we need to indicate the namespace name:

   .. code-block:: console

    # export OIO_NS=OPENIO

Most storage operations also need an account name:

   .. code-block:: console

    # export OIO_ACCOUNT=my_account

Note here that we use environment variables but you could also use the
command-line arguments ``--oio-ns`` and ``--oio-account``.


Environment variables
---------------------

The following environment variables are accepted by the `openio` command

* ``OIO_NS`` The namespace name.
* ``OIO_ACCOUNT`` The account name to use.
* ``OIO_PROXYD_URL`` Proxied URL to connect to.

Configuration files
-------------------

By default, the ``openio`` command line looks for its configuration in
``/etc/oio/sds`` and in the ``.oio`` directory within your ``$HOME``.


Account
=======

Accounts track usage about storage; they are automatically created.

Information about accounts
--------------------------

  To show information about an account, the number of containers, the number of objects, and total storage usage:

   .. code-block:: console

    # openio account show my_account

    +------------+------------------+
    | Field      | Value            |
    +------------+------------------+
    | bytes      | 0                |
    | containers | 1                |
    | ctime      | 1441108158.46772 |
    | id         | my_account       |
    | metadata   | {}               |
    | objects    | 0                |
    +------------+------------------+

List containers
---------------

  To show the list of all the containers that belong to an account:

  .. code-block:: console

    # openio container list

    +---------------+---------+-------+
    | Name          | Bytes   | Count |
    +---------------+---------+-------+
    | my_container1 |     317 |     3 |
    | my_container2 |     524 |     7 |
    | my_container3 |     171 |     1 |
    +---------------+---------+-------+

Use multiple accounts
---------------------

Specify in which account to execute actions by adding the
``--oio-account <account_name>`` parameter to your commands:

   .. code-block:: console

    # openio container create my_container --oio-account my_account_2

    +----------------+---------+
    | Name           | Created |
    +----------------+---------+
    | my_container   | True    |
    +----------------+---------+

The account ``my_account_2`` was automatically created.

   .. code-block:: console

    # openio container list --oio-account my_account_2

    +----------------+-------+-------+
    | Name           | Bytes | Count |
    +----------------+-------+-------+
    | test_container |     0 |     0 |
    +----------------+-------+-------+


You can also create manually an account:

   .. code-block:: console

    # openio account create my_account_3

Container
=========

Create a container
------------------

   .. code-block:: console

    # openio container create my_container

    +--------------+---------+
    | Name         | Created |
    +--------------+---------+
    | my_container | True    |
    +--------------+---------+

Information about container
---------------------------

Display information about this container.

   .. code-block:: console

    # openio container show my_container

    +----------------+--------------------------------------------------------------------+
    | Field          | Value                                                              |
    +----------------+--------------------------------------------------------------------+
    | account        | my_account                                                         |
    | base_name      | CB2D04216603B8274AB831F889EAA4B2656D1EBA45B658712D59C77DAC86E08A.1 |
    | bytes_usage    | 14                                                                 |
    | container      | my_container                                                       |
    | ctime          | 1441105114                                                         |
    | objects        | 1                                                                  |
    | quota          | 102400                                                             |
    | storage_policy | ERASURECODE                                                        |
    +----------------+--------------------------------------------------------------------+

You can override the storage policy for a given container on the fly:

.. code-block:: console

    # openio container create my_container2 --storage-policy=TWOCOPIES


Locate container
----------------

To find the services used by a given container:

   .. code-block:: console

    # openio container locate my_container

    +-----------+--------------------------------------------------------------------+
    | Field     | Value                                                              |
    +-----------+--------------------------------------------------------------------+
    | account   | my_account                                                         |
    | base_name | 23D6D41A55BDE4380C748B5BCDFB93085F9053F9786D4582EF0FA646286854F3.1 |
    | meta0     | 172.32.0.1:6001, 172.32.0.2:6001, 172.32.0.3:6001                  |
    | meta1     | 172.32.0.1:6002, 172.32.0.2:6002, 172.32.0.3:6002                  |
    | meta2     | 172.32.0.1:6003, 172.32.0.2:6003, 172.32.0.3:6003                  |
    | name      | my_container                                                       |
    +-----------+--------------------------------------------------------------------+

Container properties
--------------------

To set a property <key=value> to a given container:

   .. code-block:: console

    # openio container set my_container --property color=blue

Properties can be displayed with ``container show``:

   .. code-block:: console

    # openio container show my_container

    +-----------------+--------------------------------------------------------------------+
    | Field           | Value                                                              |
    +-----------------+--------------------------------------------------------------------+
    ...
    | meta.color      | blue                                                               |
    +-----------------+--------------------------------------------------------------------+

To delete a property:

   .. code-block:: console

    # openio container unset my_container --property color

Delete container
----------------

   .. code-block:: console

    # openio container delete my_container

Note: only empty containers can be deleted.

   .. code-block:: console

    Request error: Container not empty (HTTP 409) (STATUS 438)

There are still objects in the container.

First, delete all objects stored in the container.

   .. code-block:: console

    # openio object delete my_container folder_3_0 folder_2 folder_1 file2 file1 config2 config1

And finally delete the container.

   .. code-block:: console

    # openio container delete my_container

Object
======

Create an object
----------------

   .. code-block:: console

    # echo 'Hello OpenIO!' > test.txt
    # openio object create my_container test.txt

    +----------+------+----------------------------------+
    | Name     | Size | Hash                             |
    +----------+------+----------------------------------+
    | test.txt |   14 | 9EB03B6E836CEAE565BA79F76C821DDA |
    +----------+------+----------------------------------+

You can override the storage policy for a given object on the fly:

.. code-block:: console

    # openio object create my_container test2.txt --policy=TWOCOPIES


List objects
------------

   .. code-block:: console

    # openio object list my_container

    +----------+------+----------------------------------+
    | Name     | Size | Hash                             |
    +----------+------+----------------------------------+
    | test.txt |   14 | 9EB03B6E836CEAE565BA79F76C821DDA |
    +----------+------+----------------------------------+

Containers can hold a large number of objects so there are several methods to
filter the results.

Here are the optional arguments which can be used:

- ``--marker``: Indicates where to start the listing from.
- ``--end_marker``: Indicates where to end the listing.
- ``--prefix``: If set, the listing only includes objects whose name begin with its value.
- ``--delimiter``: If set, excludes objects whose name contains its value.
  Only takes a single character. It can also be combined with the ``--prefix`` for advanced listings.
- ``--limit``: Indicates the maximum number of objects to return in the listing.

To illustrate these features, create these files and store them in a container

   .. code-block:: console

    # touch folder_1 folder_2 folder_3_0 file1 file2 config1 config2
    # openio object create my_container folder_1 folder_2 folder_3_0 file1 file2 config1 config2
    [...]

To list all the objects:

   .. code-block:: console

    # openio object list my_container

    +------------+------+----------------------------------+
    | Name       | Size | Hash                             |
    +------------+------+----------------------------------+
    | config1    |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | config2    |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | file1      |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | file2      |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | folder_1   |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | folder_2   |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | folder_3_0 |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | test.txt   |   14 | 9EB03B6E836CEAE565BA79F76C821DDA |
    +------------+------+----------------------------------+

Try the filtering features.

This only outputs a maximum of three objects whose names are lexically greater than ``e``:

   .. code-block:: console

    # openio object list my_container --limit 3 --marker e

    +----------+------+----------------------------------+
    | Name     | Size | Hash                             |
    +----------+------+----------------------------------+
    | file1    |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | file2    |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | folder_1 |    0 | D41D8CD98F00B204E9800998ECF8427E |
    +----------+------+----------------------------------+

This only outputs the objects whose names begin with ``file``:

   .. code-block:: console

    # openio object list my_container --prefix file

    +-------+------+----------------------------------+
    | Name  | Size | Hash                             |
    +-------+------+----------------------------------+
    | file1 |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | file2 |    0 | D41D8CD98F00B204E9800998ECF8427E |
    +-------+------+----------------------------------+

This excludes all the objects whose names contain a ``_`` character:

   .. code-block:: console

    # openio object list my_container --delimiter _

    +----------+------+----------------------------------+
    | Name     | Size | Hash                             |
    +----------+------+----------------------------------+
    | config1  |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | config2  |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | file1    |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | file2    |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | test.txt |   14 | 9EB03B6E836CEAE565BA79F76C821DDA |
    +----------+------+----------------------------------+

This collects all the objects whose names begin with ``folder_``,
and then excludes all those whose names contain a ``_`` character after the prefix:

   .. code-block:: console

    # openio object list my_container --prefix folder_ --delimiter _

    +----------+------+----------------------------------+
    | Name     | Size | Hash                             |
    +----------+------+----------------------------------+
    | folder_1 |    0 | D41D8CD98F00B204E9800998ECF8427E |
    | folder_2 |    0 | D41D8CD98F00B204E9800998ECF8427E |
    +----------+------+----------------------------------+

Note that this can be used to emulate a hierarchy with directories.

Save object
-----------

Saves the data stored in the given object to the ``--file`` destination:

   .. code-block:: console

    # openio object save my_container test.txt --file /tmp/test.txt

If the destination file already exists, its content is deleted and replaced with this new one.

You can also save all the objects from a container to your working directory in a single command:

   .. code-block:: console

    # mkdir test_folder && cd test_folder
    # openio container save my_container
    # ls

    config1  config2  file1  file2  folder_1  folder_2  folder_3_0  test.txt

    # cd .. && rm -rf test_folder

Information about object
------------------------

Display the information about an object:

   .. code-block:: console

    # openio object show my_container test.txt

    +-----------+----------------------------------+
    | Field     | Value                            |
    +-----------+----------------------------------+
    | account   | my_account                       |
    | container | my_container                     |
    | ctime     | 1441057689                       |
    | hash      | 9EB03B6E836CEAE565BA79F76C821DDA |
    | mime-type | octet/stream                     |
    | object    | test.txt                         |
    | policy    | none                             |
    | size      | 14                               |
    +-----------+----------------------------------+

Locate object
-------------

To find the precise location of a given object:

   .. code-block:: console

    # openio object locate my_container test.txt

    +-----+------------------------------------------+------+----------------------------------+
    | Pos | Id                                       | Size | Hash                             |
    +-----+------------------------------------------+------+----------------------------------+
    | 0   | http://172.32.0.1:6001/4FCAEEF90B[...]   |  14  | 1463508F28EDB4D6D5AE349B20E00409 |
    | 0   | http://172.32.0.2:6001/7EBAD5FCB8[...]   |  14  | 1463508F28EDB4D6D5AE349B20E00409 |
    | 0   | http://172.32.0.3:6001/D425787855[...]   |  14  | 1463508F28EDB4D6D5AE349B20E00409 |
    +-----+------------------------------------------+------+----------------------------------+

``Pos`` integer represents the position of the given chunk in the object.
In case of replication, you can have multiple chunks at the same position (3 x replication mode in this example).

``Id`` is the URL to access to the given chunk.

``Size`` is the size of the given chunk.

``Hash`` is the hash of the given chunk.


Object properties
-----------------

To set a property <key=value> to a given object:

   .. code-block:: console

    # openio object set my_container test.txt --property size=small

Properties can be displayed with ``object show``:

   .. code-block:: console

    # openio object show my_container test.txt

    +-----------+----------------------------------+
    | Field     | Value                            |
    +-----------+----------------------------------+
    [...]
    | meta.size | small                            |
    [...]
    +-----------+----------------------------------+

To delete a property:

   .. code-block:: console

    # openio object unset my_container test.txt --property size

Delete objects
--------------

   .. code-block:: console

    # openio object delete my_container test.txt


Cluster management
==================

Show namespace configuration
----------------------------

To display the namespace configuration:

  .. code-block:: console

   # openio cluster show

    +----------------------------+-----------------------------------------------------------------+
    | Field                      | Value                                                           |
    +----------------------------+-----------------------------------------------------------------+
    | namespace                  | OPENIO                                                          |
    | chunksize                  | 1048576                                                         |
    | storage_policy.EC          | NONE:EC                                                         |
    | storage_policy.SINGLE      | NONE:NONE                                                       |
    | storage_policy.THREECOPIES | rawx3:DUPONETHREE                                               |
    | data_security.DUPONETHREE  | plain/distance=1,nb_copy=3                                      |
    | data_security.EC           | ec/k=6,m=3,algo=liberasurecode_rs_vand,distance=1               |
    [...]
    | storage_policy             | EC                                                              |
    +----------------------------+-----------------------------------------------------------------+


List services
-------------

To list running services in the namespace:

  .. code-block:: console

   # openio cluster list

    +---------+----------------+----------------------+----------+-------+------+-------+
    | Type    | Id             | Volume               | Location | Slots | Up   | Score |
    +---------+----------------+----------------------+----------+-------+------+-------+
    | rawx    | 127.0.0.1:6012 | /data/OPENIO-rawx-1  | oio.vol1 | rawx  | True |    86 |
    | rawx    | 127.0.0.1:6013 | /data/OPENIO-rawx-2  | oio.vol2 | rawx  | True |    86 |
    | rawx    | 127.0.0.1:6014 | /data/OPENIO-rawx-3  | oio.vol3 | rawx  | True |    86 |
    [...]
    | meta2   | 127.0.0.1:6006 | /data/OPENIO-meta2-1 | oio.vol1 | meta2 | True |    86 |
    | meta2   | 127.0.0.1:6007 | /data/OPENIO-meta2-2 | oio.vol2 | meta2 | True |    86 |
    | meta2   | 127.0.0.1:6008 | /data/OPENIO-meta2-3 | oio.vol3 | meta2 | True |    85 |
    | meta1   | 127.0.0.1:6005 | /data/OPENIO-meta1-1 | oio.vol1 | meta1 | True |    85 |
    | meta0   | 127.0.0.1:6004 | /data/OPENIO-meta0-1 | oio.vol1 | meta0 | True |    85 |
    +---------+----------------+----------------------+----------+-------+------+-------+



By default, ``cluster list`` displays all known services.

To list only specific types of services:

  .. code-block:: console

   # openio cluster list rawx meta2

    +---------+----------------+----------------------+----------+-------+------+-------+
    | Type    | Id             | Volume               | Location | Slots | Up   | Score |
    +---------+----------------+----------------------+----------+-------+------+-------+
    | rawx    | 127.0.0.1:6012 | /data/OPENIO-rawx-1  | oio.vol1 | rawx  | True |    86 |
    | rawx    | 127.0.0.1:6013 | /data/OPENIO-rawx-2  | oio.vol2 | rawx  | True |    86 |
    | rawx    | 127.0.0.1:6014 | /data/OPENIO-rawx-3  | oio.vol3 | rawx  | True |    86 |
    [...]
    | meta2   | 127.0.0.1:6006 | /data/OPENIO-meta2-1 | oio.vol1 | meta2 | True |    86 |
    | meta2   | 127.0.0.1:6007 | /data/OPENIO-meta2-2 | oio.vol2 | meta2 | True |    86 |
    | meta2   | 127.0.0.1:6008 | /data/OPENIO-meta2-3 | oio.vol3 | meta2 | True |    85 |
    +---------+----------------+----------------------+----------+-------+------+-------+

Local configuration
-------------------

To display local namespace configuration:

  .. code-block:: console

   # openio cluster local conf

    +--------------------+-----------------------------+
    | Field              | Value                       |
    +--------------------+-----------------------------+
    | OPENIO/conscience  | 127.0.0.1:6002              |
    | OPENIO/zookeeper   | 127.0.0.1:2181              |
    | OPENIO/proxy       | 127.0.0.1:6000              |
    | OPENIO/ecd         | 127.0.0.1:6001              |
    | OPENIO/event-agent | beanstalk://127.0.0.1:11300 |
    +--------------------+-----------------------------+

Score management
----------------

The first time a service is discovered in the namespace, its score is locked at 0.

To unlock a new service:

  .. code-block:: console

   # openio cluster unlock rawx 127.0.0.1:6015

    +------+----------------+----------+
    | Type | Service        | Result   |
    +------+----------------+----------+
    | rawx | 127.0.0.1:6015 | unlocked |
    +------+----------------+----------+

To unlock all registered services:

  .. code-block:: console

   # openio cluster unlockall

    +-------+----------------+----------+
    | Type  | Service        | Result   |
    +-------+----------------+----------+
    | meta2 | 127.0.0.1:6006 | unlocked |
    | meta2 | 127.0.0.1:6007 | unlocked |
    | meta2 | 127.0.0.1:6008 | unlocked |
    [...]
    | rawx  | 127.0.0.1:6014 | unlocked |
    | rawx  | 127.0.0.1:6015 | unlocked |
    +-------+----------------+----------+
