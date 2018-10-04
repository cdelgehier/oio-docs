.. title:: Integrate Open-XChange Dovecot (Enterprise Edition) with on premise Swift/S3 object storage.

.. _ref-use-case-dovecot:

============
Dovecot Obox
============

Description
-----------

Dovecot Obox is a dovecot plugin available in Dovecot Pro.
It adds support to Dovecot for mail storage in object storage.

This guide will explain how to configure dovecot to use OpenIO.

Prerequisites
-------------

* Dovecot Pro installed and setup.
* OpenIO cluster configured with the Swift/S3 proxy.

Bucket is configured to be accessed using virtual addressing (eg. `http://mybucket.openio.localdomain:6007`).

Have these values ready:

* Bucket URL `BUCKET_URL`
* Access key `ACCESS_KEY`
* Secret access key `SECRET_ACCESS_KEY`


Configuration
-------------

Create a new file `/etc/dovecot/conf.d/11-obox.conf`:

.. code-block:: cfg

  mail_plugins = $mail_plugins obox

  mail_location = obox:%2Mu/%2.3Mu/%u:INDEX=~/:CONTROL=~/

  plugin {
    obox_use_object_ids = yes

    obox_fs = fscache 1G:/var/cache/dovecot:s3:http://ACCESS_KEY:SECRET_ACCESS_KEY@BUCKET_URL
  }


Apply the changes by reloading dovecot configuration:

.. code-block:: console

  $ sudo doveconf reload
