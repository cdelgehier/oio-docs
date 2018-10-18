=================
Metadata Indexing
=================

Metadata indexing uses Functions to provide indexing and search of metadata in OpenIO SDS.

Index creation
--------------

An index is automatically created when inserting a first document. A mapping type is automatically associated to it thanks to the index template.

Index name
++++++++++

With `$acc` being the SDS account name, the corresponding index name is `"oio_"+b32($acc).lower()`. This is due to the Elasticsearch index naming constraints ([see](https://stackoverflow.com/a/41585755/2211877)).


Functions
---------

Functions are configured via environment variables:

* `ES_ADDR`: *(mandatory)* The elasticsearch address.
* `KS_ADDR`: *(mandatory for the search)* The keystone address.
* `RESELLER_PREFIX`: The prefix added to the account name by swift. Default: `AUTH_`.
* `INDEX_PREFIX`: The prefix added to the Elasticsearch indexes. Default: `oio_`. If changed, the index template must also be changed.
* `MAPPING_NAME`: The name of the mapping used in Elasticsearch. Default: `object`. If changed, the index template must also be changed.
* `AUTH_HOST_KEEP_PORT`: Whether or not to remove the port from the Host header when verifying the signature. Default behavior is to remove it. If the variable is set (to any value), it will be kept.
