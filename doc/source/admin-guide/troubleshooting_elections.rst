===============================
Troubleshooting Election Issues
===============================

The problem
-----------

You just wanted to set a property on a container, but something went wrong.

  .. code-block:: console

    > openio container set FVE0 --property a=1
    Open/lock: Election failed [697ECB056A5F9339B36C3B0A020B5AB17B4B0160FBEBEA203315EA1FC1B61605.1][meta2] (HTTP 503) (STATUS 503)

You check meta2 logs, but they don't really help you.

  .. code::

    Oct 10 17:26:59.829349 linux-cgzg OIO,NS,meta2,1[29617]: 29617 C448 log WRN oio.sqlite TIMEOUT! (waiting for election status) [697ECB056A5F9339B36C3B0A020B5AB17B4B0160FBEBEA203315EA1FC1B61605.1.meta2] step=6/CHECKING_SLAVES
    Oct 10 17:26:59.829420 linux-cgzg OIO,NS,meta2,1[29617]: 29617 C448 access INF 127.0.0.1:6015 127.0.0.1:34710 DB_PSET 503 5001321 168 697ECB056A5F9339B36C3B0A020B5AB17B4B0160FBEBEA203315EA1FC1B61605 C26A69B0F22EF0D8A0D635D9EBD639F7 t=5001294 697ECB056A5F9339B36C3B0A020B5AB17B4B0160FBEBEA203315EA1FC1B61605.1.meta2 e=(503) Open/lock: Election failed [697ECB056A5F9339B36C3B0A020B5AB17B4B0160FBEBEA203315EA1FC1B61605.1][meta2]


Getting information
-------------------

Since openio-sds 4.2.0, there is a CLI for election troubleshooting.
You can reproduce the election issue by running ``openio election status``,
with the type of the problematic service, and the name of the container
(alternatively, instead of the name of the container, you can use the option
``--cid`` and the name of the base). The purpose of this command is to get
the status of an election, triggering it if necessary.

  .. code-block:: console

    > openio election status meta2 FVE0
    +----------------+--------+----------------------------------------------------------------------------------------------+
    | Id             | Status | Message                                                                                      |
    +----------------+--------+----------------------------------------------------------------------------------------------+
    | 127.0.0.1:6015 |    500 | Election failed for 697ECB056A5F9339B36C3B0A020B5AB17B4B0160FBEBEA203315EA1FC1B61605.1.meta2 |
    | 127.0.0.1:6017 |      7 | Timeout                                                                                      |
    | 127.0.0.1:6018 |      7 | Timeout                                                                                      |
    +----------------+--------+----------------------------------------------------------------------------------------------+

Here an election is failing because two services do not answer fast enough.

Another interesting command is ``openio election debug`` (using the same
parameters as ``openio election status``). This returns advanced
information about the current status of an election, such as the history
of internal election states, and which event triggered state changes.

  .. code-block:: console

    > openio election debug meta2 FVE0
    +----------------+--------+------------------------------------------------+---------------------------------------------------------------------------------------+
    | Id             | Status | Message                                        | Body                                                                                  |
    +----------------+--------+------------------------------------------------+---------------------------------------------------------------------------------------+
    | 127.0.0.1:6015 |    200 | OK                                             | {                                                                                     |
    |                |        |                                                |     "#": {                                                                            |
    |                |        |                                                |         "P": 0,                                                                       |
    |                |        |                                                |         "R": 8,                                                                       |
    |                |        |                                                |         "V": 0                                                                        |
    |                |        |                                                |     },                                                                                |
    |                |        |                                                |     "base": {                                                                         |
    |                |        |                                                |         "name": "697ECB056A5F9339B36C3B0A020B5AB17B4B0160FBEBEA203315EA1FC1B61605.1", |
    |                |        |                                                |         "type": "meta2",                                                              |
    |                |        |                                                |         "zk": "D9EAF7894DB54D52FDA5A0CCC26FF3E3EE2731FEDD9944B06298A22C6BE5FCD5"      |
    |                |        |                                                |     },                                                                                |
    |                |        |                                                |     "local": {                                                                        |
    |                |        |                                                |         "id": null,                                                                   |
    |                |        |                                                |         "state": "NONE",                                                              |
    |                |        |                                                |         "url": "127.0.0.1:6015"                                                       |
    |                |        |                                                |     },                                                                                |
    |                |        |                                                |     "log": [                                                                          |
    |                |        |                                                |         "LEAVING_FAILING:LEAVE_OK:FAILED",                                            |
    |                |        |                                                |         "LEAVING_FAILING:LEFT_SELF:LEAVING_FAILING",                                  |
    |                |        |                                                |         "CHECKING_SLAVES:GETVERS_KO:LEAVING_FAILING",                                 |
    |                |        |                                                |         "CHECKING_SLAVES:GETVERS_KO:CHECKING_SLAVES",                                 |
    |                |        |                                                |         "CHECKING_SLAVES:GETVERS_KO:CHECKING_SLAVES",                                 |
    |                |        |                                                |         "CHECKING_SLAVES:GETVERS_KO:CHECKING_SLAVES",                                 |
    |                |        |                                                |         "CHECKING_SLAVES:GETVERS_KO:CHECKING_SLAVES",                                 |
    |                |        |                                                |         "CHECKING_SLAVES:GETVERS_KO:CHECKING_SLAVES",                                 |
    |                |        |                                                |         "LISTING:LIST_OK:CHECKING_SLAVES",                                            |
    |                |        |                                                |         "WATCHING:EXISTS_OK:LISTING",                                                 |
    |                |        |                                                |         "CREATING:CREATE_OK:WATCHING",                                                |
    |                |        |                                                |         "NONE:NONE:CREATING"                                                          |
    |                |        |                                                |     ],                                                                                |
    |                |        |                                                |     "master": {                                                                       |
    |                |        |                                                |         "id": null,                                                                   |
    |                |        |                                                |         "url": null                                                                   |
    |                |        |                                                |     },                                                                                |
    |                |        |                                                |     "peers": [                                                                        |
    |                |        |                                                |         "127.0.0.1:6017",                                                             |
    |                |        |                                                |         "127.0.0.1:6018"                                                              |
    |                |        |                                                |     ]                                                                                 |
    |                |        |                                                | }                                                                                     |
    | 127.0.0.1:6017 |      2 | 127.0.0.1:6017: [errno=111] Connection refused |                                                                                       |
    | 127.0.0.1:6018 |      7 | Timeout                                        |                                                                                       |
    +----------------+--------+------------------------------------------------+---------------------------------------------------------------------------------------+


Repairing
---------

If you see any loop in the history of internal election states ("log"),
the best thing to do is to ask the services to leave the election
(in the example above, the only working service has already left).

  .. code-block:: console

    > openio election leave meta2 FVE0
    +----------------+--------+------------------------------------------------+
    | Id             | Status | Message                                        |
    +----------------+--------+------------------------------------------------+
    | 127.0.0.1:6015 |      2 | 127.0.0.1:6015: [errno=111] Connection refused |
    | 127.0.0.1:6017 |      7 | Timeout                                        |
    | 127.0.0.1:6018 |    200 | OK                                             |
    +----------------+--------+------------------------------------------------+


By chance, one of the failing services is up again, and the election can now
reach a stable state.

  .. code-block:: console

    > election status meta2 FVE0
    +----------------+--------+------------------------------------------------+
    | Id             | Status | Message                                        |
    +----------------+--------+------------------------------------------------+
    | 127.0.0.1:6015 |      2 | 127.0.0.1:6015: [errno=111] Connection refused |
    | 127.0.0.1:6017 |    303 | 127.0.0.1:6018                                 |
    | 127.0.0.1:6018 |    200 | OK                                             |
    +----------------+--------+------------------------------------------------+

Status 303 indicates that the master service is 127.0.0.1:6018, and that
127.0.0.1:6017 will redirect all writes to it.
