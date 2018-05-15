.. _label-s3-compliancy:

=============
S3 Compliancy
=============

OpenIO SDS {{RELEASE}} is compliant with the most recent standards of requests signatures:

- `Amazon S3 Signature v2 <https://docs.aws.amazon.com/fr_fr/general/latest/gr/signature-version-2.html>`_
- `Amazon S3 Signature v4 <https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-authenticating-requests.html>`_

In addition to the traditional path-style bucket naming, OpenIO SDS also
complies with the host-style bucket naming as described in
`Virtual Hosting of Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/VirtualHosting.html>`_.

Here is the detail of supported operations.

.. list-table:: Common operations
   :class: s3-table
   :widths: 10 1

   * - GET Service
     - ✅


.. list-table:: Bucket operations
   :class: s3-table
   :widths: 10 1

   * - DELETE Bucket
     - ✅
   * - DELETE Bucket analytics
     - ❌
   * - DELETE Bucket cors
     - ❌
   * - DELETE Bucket encryption
     - ❌
   * - DELETE Bucket inventory
     - ❌
   * - DELETE Bucket lifecycle
     - ✅
   * - DELETE Bucket metrics
     - ❌
   * - DELETE Bucket policy
     - ❌
   * - DELETE Bucket replication
     - ❌
   * - DELETE Bucket tagging
     - ❌
   * - DELETE Bucket website
     - ❌
   * - GET Bucket (List Objects) Version 2
     - ✅
   * - GET Bucket accelerate
     - ❌
   * - GET Bucket acl
     - ✅
   * - GET Bucket analytics
     - ❌
   * - GET Bucket cors
     - ❌
   * - GET Bucket encryption
     - ❌
   * - GET Bucket Inventory
     - ❌
   * - GET Bucket lifecycle
     - ✅
   * - GET Bucket location
     - ✅
   * - GET Bucket logging
     - ❌
   * - GET Bucket metrics
     - ❌
   * - GET Bucket notification
     - ❌
   * - GET Bucket Object versions
     - ✅
   * - GET Bucket policy
     - ❌
   * - GET Bucket replication
     - ❌
   * - GET Bucket requestPayment
     - ❌
   * - GET Bucket tagging
     - ❌
   * - GET Bucket versioning
     - ✅
   * - GET Bucket website
     - ❌
   * - HEAD Bucket
     - ✅
   * - List Bucket Analytics Configurations
     - ❌
   * - List Bucket Inventory Configurations
     - ❌
   * - List Bucket Metrics Configurations
     - ❌
   * - List Multipart Uploads
     - ✅
   * - PUT Bucket
     - ✅
   * - PUT Bucket accelerate
     - ❌
   * - PUT Bucket acl
     - ✅
   * - PUT Bucket analytics
     - ❌
   * - PUT Bucket cors
     - ❌
   * - PUT Bucket encryption
     - ❌
   * - PUT Bucket inventory
     - ❌
   * - PUT Bucket lifecycle
     - ✅
   * - PUT Bucket logging
     - ❌
   * - PUT Bucket metrics
     - ❌
   * - PUT Bucket notification
     - ❌
   * - PUT Bucket policy
     - ❌
   * - PUT Bucket replication
     - ❌
   * - PUT Bucket requestPayment
     - ❌
   * - PUT Bucket tagging
     - ❌
   * - PUT Bucket versioning
     - ✅
   * - PUT Bucket website
     - ❌


.. list-table:: Objects operations
   :class: s3-table
   :widths: 10 1

   * - Delete Multiple Objects
     - ✅
   * - DELETE Object
     - ✅
   * - DELETE Object tagging
     - ❌
   * - GET Object
     - ✅
   * - GET Object ACL
     - ✅
   * - GET Object tagging
     - ❌
   * - GET Object torrent
     - ❌
   * - HEAD Object
     - ✅
   * - OPTIONS object
     - ❌
   * - POST Object
     - ❌
   * - POST Object restore
     - ❌
   * - PUT Object
     - ✅
   * - PUT Object - Copy
     - ✅
   * - PUT Object acl
     - ✅
   * - PUT Object tagging
     - ❌
   * - SELECT Object Content (Preview)
     - ❌

.. list-table:: Multiparts objects operations
   :class: s3-table
   :widths: 10 1

   * - Abort Multipart Upload
     - ✅
   * - Complete Multipart Upload
     - ✅
   * - Initiate Multipart Upload
     - ✅
   * - List Parts
     - ✅
   * - Upload Part
     - ✅
   * - Upload Part - Copy
     - ✅

