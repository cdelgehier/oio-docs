======
RClone
======

Description
-----------

Rclone is a cloud backup tool.
It can sync to and from various cloud storage backends, and can be used on Windows/macOS/Linux.
It supports OpenIO object storage via S3.

This guide will explain how to setup a new remote in Rclone to use OpenIO.

Prerequisites
-------------

In the present guide, we expect **Rclone** to be installed.

It also expects that you have configured access to an OpenIO cluster with the S3 gateway.
You must know your S3 credentials (access_key and secret_access_key) and the S3 endpoint URL.

Use these values with the openio/sds docker container:

* Endpoint URL (http://localhost:6007)
* Access key (demo:demo)
* Secret access key (DEMO_PASS)

Please `contact us <https://info.openio.io/request-information>`_ for additional information
about our preferred S3 setup.


Configuration
-------------

Configure a new openio remote. First, we call the `rclone` configuration tool:

.. code-block:: console

   $ rclone config
   Current remotes:

   Name                 Type
   ====                 ====
   gcs                  google cloud storage
   s3                   s3

   e) Edit existing remote
   n) New remote
   d) Delete remote
   r) Rename remote
   c) Copy remote
   s) Set configuration password
   q) Quit config

Add a new remote:

.. code-block:: console

   e/n/d/r/c/s/q> n

Name the new remote:

.. code-block:: console

   name> openio
   Type of storage to configure.
   Choose a number from below, or type in your own value
    1 / Amazon Drive
      \ "amazon cloud drive"
    2 / Amazon S3 (also Dreamhost, Ceph, Minio)
      \ "s3"
    3 / Backblaze B2
      \ "b2"
    4 / Box
      \ "box"
    5 / Dropbox
      \ "dropbox"
    6 / Encrypt/Decrypt a remote
      \ "crypt"
    7 / FTP Connection
      \ "ftp"
    8 / Google Cloud Storage (this is not Google Drive)
      \ "google cloud storage"
    9 / Google Drive
      \ "drive"
   10 / Hubic
      \ "hubic"
   11 / Local Disk
      \ "local"
   12 / Microsoft Azure Blob Storage
      \ "azureblob"
   13 / Microsoft OneDrive
      \ "onedrive"
   14 / Openstack Swift (Rackspace Cloud Files, Memset Memstore, OVH)
      \ "swift"
   15 / QingClound Object Storage
      \ "qingstor"
   16 / SSH/SFTP Connection
      \ "sftp"
   17 / Yandex Disk
      \ "yandex"
   18 / http Connection
      \ "http"

The new remote uses the S3 protocol:

.. code-block:: console

   Storage> 2
   Get AWS credentials from runtime (environment variables or EC2 meta data if no env vars). Only applies if access_key_id and secret_access_key is blank.
   Choose a number from below, or type in your own value
    1 / Enter AWS credentials in the next step
      \ "false"
    2 / Get AWS credentials from the environment (env vars or IAM)
      \ "true"


Explicit the S3 credentials:

.. code-block:: console

   env_auth> 1
   AWS Access Key ID - leave blank for anonymous access or runtime credentials.
   access_key_id> demo:demo
   AWS Secret Access Key (password) - leave blank for anonymous access or runtime credentials.
   Region to connect to.
   Choose a number from below, or type in your own value
      / The default endpoint - a good choice if you are unsure.
    1 | US Region, Northern Virginia or Pacific Northwest.
      | Leave location constraint empty.
      \ "us-east-1"
      / US East (Ohio) Region
    2 | Needs location constraint us-east-2.
      \ "us-east-2"
      / US West (Oregon) Region
    3 | Needs location constraint us-west-2.
      \ "us-west-2"
      / US West (Northern California) Region
    4 | Needs location constraint us-west-1.
      \ "us-west-1"
      / Canada (Central) Region
    5 | Needs location constraint ca-central-1.
      \ "ca-central-1"
      / EU (Ireland) Region
    6 | Needs location constraint EU or eu-west-1.
      \ "eu-west-1"
      / EU (London) Region
    7 | Needs location constraint eu-west-2.
      \ "eu-west-2"
      / EU (Frankfurt) Region
    8 | Needs location constraint eu-central-1.
      \ "eu-central-1"
      / Asia Pacific (Singapore) Region
    9 | Needs location constraint ap-southeast-1.
      \ "ap-southeast-1"
      / Asia Pacific (Sydney) Region
   10 | Needs location constraint ap-southeast-2.
      \ "ap-southeast-2"
      / Asia Pacific (Tokyo) Region
   11 | Needs location constraint ap-northeast-1.
      \ "ap-northeast-1"
      / Asia Pacific (Seoul)
   12 | Needs location constraint ap-northeast-2.
      \ "ap-northeast-2"
      / Asia Pacific (Mumbai)
   13 | Needs location constraint ap-south-1.
      \ "ap-south-1"
      / South America (Sao Paulo) Region
   14 | Needs location constraint sa-east-1.
      \ "sa-east-1"
      / If using an S3 clone that only understands v2 signatures
   15 | eg Ceph/Dreamhost
      | set this and make sure you set the endpoint.
      \ "other-v2-signature"
      / If using an S3 clone that understands v4 signatures set this
   16 | and make sure you set the endpoint.
      \ "other-v4-signature"

Explicit the S3 endpoint:

.. code-block:: console

   region> 15
   Endpoint for S3 API.
   Leave blank if using AWS to use the default endpoint for the region.
   Specify if using an S3 clone such as Ceph.
   endpoint> http://localhost:6007
   Location constraint - must be set to match the Region. Used when creating buckets only.
   Choose a number from below, or type in your own value
    1 / Empty for US Region, Northern Virginia or Pacific Northwest.
      \ ""
    2 / US East (Ohio) Region.
      \ "us-east-2"
    3 / US West (Oregon) Region.
      \ "us-west-2"
    4 / US West (Northern California) Region.
      \ "us-west-1"
    5 / Canada (Central) Region.
      \ "ca-central-1"
    6 / EU (Ireland) Region.
      \ "eu-west-1"
    7 / EU (London) Region.
      \ "eu-west-2"
    8 / EU Region.
      \ "EU"
    9 / Asia Pacific (Singapore) Region.
      \ "ap-southeast-1"
   10 / Asia Pacific (Sydney) Region.
      \ "ap-southeast-2"
   11 / Asia Pacific (Tokyo) Region.
      \ "ap-northeast-1"
   12 / Asia Pacific (Seoul)
      \ "ap-northeast-2"
   13 / Asia Pacific (Mumbai)
      \ "ap-south-1"
   14 / South America (Sao Paulo) Region.
      \ "sa-east-1"

No region is set by default; you must explicit it here:

.. code-block:: console

   location_constraint> 1
   Canned ACL used when creating buckets and/or storing objects in S3.
   For more info visit https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl
   Choose a number from below, or type in your own value
    1 / Owner gets FULL_CONTROL. No one else has access rights (default).
      \ "private"
    2 / Owner gets FULL_CONTROL. The AllUsers group gets READ access.
      \ "public-read"
      / Owner gets FULL_CONTROL. The AllUsers group gets READ and WRITE access.
    3 | Granting this on a bucket is generally not recommended.
      \ "public-read-write"
    4 / Owner gets FULL_CONTROL. The AuthenticatedUsers group gets READ access.
      \ "authenticated-read"
      / Object owner gets FULL_CONTROL. Bucket owner gets READ access.
    5 | If you specify this canned ACL when creating a bucket, Amazon S3 ignores it.
      \ "bucket-owner-read"
      / Both the object owner and the bucket owner get FULL_CONTROL over the object.
    6 | If you specify this canned ACL when creating a bucket, Amazon S3 ignores it.
      \ "bucket-owner-full-control"


Next, explicit the S3 endpoint, and you will have full control over its location.

.. code-block:: console

   acl> 1
   The server-side encryption algorithm used when storing this object in S3.
   Choose a number from below, or type in your own value
    1 / None
      \ ""
    2 / AES256
      \ "AES256"

Choose the appropriate encryption algorithm:

.. code-block:: console

   server_side_encryption> 1
   The storage class to use when storing objects in S3.
   Choose a number from below, or type in your own value
    1 / Default
      \ ""
    2 / Standard storage class
      \ "STANDARD"
    3 / Reduced redundancy storage class
      \ "REDUCED_REDUNDANCY"
    4 / Standard Infrequent Access storage class
      \ "STANDARD_IA"

No storage class is necessary at this point.

.. code-block:: console

   storage_class> 1
   Remote config
   --------------------
   [openio]
   env_auth = false
   access_key_id = demo:demo
   secret_access_key = DEMO_PASS
   region = other-v2-signature
   endpoint = http://localhost:6007
   location_constraint =
   acl = private
   server_side_encryption =
   storage_class =
   --------------------
   y) Yes this is OK
   e) Edit this remote
   d) Delete this remote

You are done.

.. code-block:: console

   y/e/d> y


Commands
--------

`rclone` is now ready to use, the new remote is called openio. Let’s see how we can use it.

List all buckets

.. code-block:: console

   $ rclone lsd openio:

Create a new bucket

.. code-block:: console

   $ rclone mkdir openio:mybucket

List the contents of a bucket

.. code-block:: console

   $ rclone ls openio:mybucket

Sync /home/user/documents to a bucket

.. code-block:: console

   $ rclone sync /home/user/documents openio:mybucket

Copy a file /home/user/file.txt to a bucket

.. code-block:: console

   $ rclone copy `/home/user/file.txt` openio:mybucket

Download a file file.txt from a bucket

.. code-block:: console

   $ rclone copy openio:mybucket/file.txt file.txt

Sync a bucket from a different remote to OpenIO

.. code-block:: console

   $ rclone sync remote:myoldbucket openio:mybucket

Note that this requires downloading and uploading the data from the machine running Rclone.
