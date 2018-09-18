=============================
Back Up & Restore a Container
=============================

Preparation
~~~~~~~~~~~

You must stop all activities on the container during the creation of the backup.

Backup
~~~~~~

A container backup can be done with a single operation:

.. code-block:: shell

    $ curl 'http://SERVEUR:PORT/v1.0/container/dump?acct=ACCOUNT&ref=CONTAINER' --output CONTAINER.tar

Or it can be split in several operations:

.. code-block:: shell

    $ export URL='http://SERVEUR:PORT/v1.0/container/dump?acct=ACCOUNT&ref=CONTAINER'
    $ curl -I "$URL"
    HTTP/1.1 200 OK
    Date: Fri, 30 Jun 2017 08:43:22 GMT
    Server: Apache
    Content-Length: 2107904
    X-Blocks: 4117
    Accept-Ranges: bytes
    Content-Type: application/tar
    $ curl -H 'Range: bytes=0-1023999' "$URL" > CONTAINER_part1.tar
    $ curl -H 'Range: bytes=1024000-2047999' "$URL" > CONTAINER_part2.tar
    $ curl -H 'Range: bytes=2048000-2107903' "$URL" > CONTAINER_part3.tar

**Note:**

- Range must be a multiple of 512 bytes
- Properties of objects are saved as extended attributes
- Backing up a S3 bucket with Static Large Object will aggregate segments to expose one unique file.

Using Backup
~~~~~~~~~~~~

A backup can be tested on a Linux filesystem with the tar utility, using the --ignore-zeros option

.. code-block:: shell

    $ tar tfiv CONTAINER.tar
    .__oio_container_manifest
    tar: Ignoring unknown extended header keyword 'mime_type'
    .__oio_container_properties
    tar: Ignoring unknown extended header keyword 'mime_type'
    32M
    tar: Ignoring unknown extended header keyword 'mime_type'
    group
    tar: Ignoring unknown extended header keyword 'mime_type'
    passwd
    tar: Ignoring unknown extended header keyword 'mime_type'
    hosts

To extract a tar and keep properties on files:

.. code-block:: shell

    $ tar xvfi a.tar --xattrs
    .__oio_container_manifest
    tar: Ignoring unknown extended header keyword 'mime_type'
    32M
    tar: Ignoring unknown extended header keyword 'mime_type'
    group
    tar: Ignoring unknown extended header keyword 'mime_type'
    passwd
    tar: Ignoring unknown extended header keyword 'mime_type'
    zzz
    $ xattr -l 32M
    user.a15: a15
    user.a48: a48
    user.a49: a49
    user.a1: a1
    $ openio object show CONTAINER 32M
    +-----------+----------------------------------+
    | Field     | Value                            |
    +-----------+----------------------------------+
    | account   | ACCOUNT                          |
    | container | CONTAINER                        |
    | ctime     | 1498730138                       |
    | hash      |                                  |
    | id        | C1F47E4D165305005B1040FAC82617E2 |
    | meta.a15  | a15                              |
    | meta.a48  | a48                              |
    | meta.a49  | a49                              |
    +-----------+----------------------------------+

**Notes:**

- The file `.__oio_container_manifest` describe the mapping of the container during download.
- The file `.__oio_container_properties` contains properties applied on the container itself.
- Each file has a mime_type attribute, only used by a restore operation.

Restore
~~~~~~~

As with backups, a restore can be done with a single operation:

.. code-block:: shell

    $ curl -XPUT --data-binary @CONTAINER.tar 'http://SERVEUR:PORT/v1.0/container/restore?acct=ACCOUNT&ref=NEW_CONTAINER'

Or it can be split into several smaller upload operations (the order must be respected):

.. code-block:: shell

    $ export URL='http://SERVEUR:PORT/v1.0/container/restore?acct=ACCOUNT&ref=NEW_CONTAINER'
    $ curl -XPUT -H 'Range: bytes=0-1023999' --data-binary @CONTAINER_part1.tar "$URL"
    $ curl -XPUT -H 'Range: bytes=1024000-2047999' --data-binary @CONTAINER_part2.tar "$URL"
    $ curl -XPUT -H 'Range: bytes=2048000-2107903' --data-binary @CONTAINER_part3.tar "$URL"

**Notes:**

- Parts must be multiple of 1 MiB. Padding is used in backup files to avoid splitting block headers.
- The upload of a tar archive without .__oio_container_manifest using multi part upload is not supported.
- it is not recommended to alter a tar archive (extracting then recompressing for example) as `.__oio_container_manifest` will be invalid
- it is possible to upload any tar archive using the single shot method. The archive must contain only regular files and directory entries; special files or links are not supported.
