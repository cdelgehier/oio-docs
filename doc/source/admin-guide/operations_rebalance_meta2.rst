=========================
Rebalance a volume: meta2
=========================
.. sectionauthor:: murlock
.. contents::
   :depth: 1
   :local:

OpenIO advises you not to use this procedure. The risk of data loss is real,
if mishandling especially the specifications of IP addresses.


Prepare environnment
++++++++++++++++++++

::

    export OIO_NS=$NS
    export OIO_ACCOUNT=account
    export PROXY=LocalIPofProxy

    export NS=$OIO_NS
    export ACCOUNT=$OIO_ACCOUNT
    export CNT=cnt2


Retrieve DB name and list of associated meta2 server
++++++++++++++++++++++++++++++++++++++++++++++++++++

::

    $ openio container show $CNT | grep base_name
    | base_name      | E11A2CF2E8001309E9500E644836C8F050A0BB9CD39F10276B44AD30B4AABC99.1 |

    $ openio reference list $CNT
    +-------+----------------+------+-----+
    | Type  | Host           | Args | Seq |
    +-------+----------------+------+-----+
    | meta2 | 127.0.0.1:6023 |      |   1 |
    | meta2 | 127.0.0.3:6025 |      |   1 |
    | meta2 | 127.0.0.1:6020 |      |   1 |
    +-------+----------------+------+-----+


Retrieve DB location and prepare new reference
++++++++++++++++++++++++++++++++++++++++++++++

::

    $ openio cluster list meta2 | grep -E '(127.0.0.1:6023|127.0.0.1:6025|127.0.0.2:6020)'
    | meta2 | 127.0.0.2:6023 | /home/murlock/.oio/sds/data/OPENIO-meta2-2 | srv2.vol2 | meta2 | True  |    67 |
    | meta2 | 127.0.0.1:6025 | /home/murlock/.oio/sds/data/OPENIO-meta2-4 | srv1.vol4 | meta2 | True  |    67 |
    | meta2 | 127.0.0.1:6020 | /home/murlock/.oio/sds/data/OPENIO-meta2-7 | srv1.vol7 | meta2 | False |     0 |

    $ export NEWMETA2=127.0.0.1:6023,127.0.0.3:6025,127.0.0.2:6024


Flush proxy cache on cluster
++++++++++++++++++++++++++++

::

    for proxy in PROXY1 PROXY2 PROXY3; do
        curl -X POST "http://$proxy/v3.0/cache/flush/low"
        curl -X POST "http://$proxy/v3.0/cache/flush/high"
    done


Force election LEAVE
++++++++++++++++++++

::

    $ curl -XPOST "http://$PROXY/v3.0/$NS/admin/leave?acct=$ACCOUNT&ref=$CNT&type=meta2" | python -m json.tool
    {
        "127.0.0.1:6020": {
            "body": "",
            "status": {
                "message": "OK",
                "status": 200
            }
        },
        "127.0.0.1:6023": {
            "body": "",
            "status": {
                "message": "OK",
                "status": 200
            }
        },
        "127.0.0.3:6025": {
            "body": "",
            "status": {
                "message": "OK",
                "status": 200
            }
        }
    }


Remove reference of meta2
+++++++++++++++++++++++++

::

    $ openio reference unlink $CNT meta2


Freeze and backup DB
++++++++++++++++++++

::

    $ curl -XPOST "http://$PROXY/v3.0/$NS/admin/freeze?acct=$ACCOUNT&ref=$CNT&type=meta2" -d ''
    {}
    $ scp 127.0.0.2:6023 "sqlite3 /home/murlock/.oio/sds/data/OPENIO-meta2-2/E11/E11A2CF2E8001309E9500E644836C8F050A0BB9CD39F10276B44AD30B4AABC99.1.meta2 .


Update peers manually in DB
+++++++++++++++++++++++++++

::

    ssh 127.0.0.2:6023 "sqlite3 /home/murlock/.oio/sds/data/OPENIO-meta2-2/E11/E11A2CF2E8001309E9500E644836C8F050A0BB9CD39F10276B44AD30B4AABC99.1.meta2 "update admin set v = '$NEWMETA2' where k='sys.peers'"
    ssh 127.0.0.1:6025 "sqlite3 /home/murlock/.oio/sds/data/OPENIO-meta2-4/E11/E11A2CF2E8001309E9500E644836C8F050A0BB9CD39F10276B44AD30B4AABC99.1.meta2 "update admin set v = '$NEWMETA2' where k='sys.peers'"


Enable DB
+++++++++

::

    $ curl -XPOST "http://$PROXY/v3.0/$NS/admin/enable?acct=$ACCOUNT&ref=$CNT&type=meta2" -d ''
    {}


Add updated reference of meta2
++++++++++++++++++++++++++++++

::

    $ openio reference force $CNT $NEWMETA2 meta2


Check state of election
+++++++++++++++++++++++

The hosts should be the new ones but still with decommissioned value0 in peer
field

::

    $ curl -XPOST "http://$PROXY/v3.0/$NS/admin/debug?acct=$ACCOUNT&ref=$CNT&type=meta2"
    {
        "127.0.0.1:6023": {
            "body": {
                "#": {
                    "getvers": 0,
                    "pipefrom": 0,
                    "refcount": 2
                },
                "base": {
                    "name": "E11A2CF2E8001309E9500E644836C8F050A0BB9CD39F10276B44AD30B4AABC99.1",
                    "type": "meta2",
                    "zk": "7353556D83E9E1F88E851072150B0B87DB537C128E2271CC4E8F014051EB9B28"
                },
                "local": {
                    "id": null,
                    "state": "NONE",
                    "url": "127.0.0.1:6023"
                },
                "log": [
                    "1529938978925:LEAVING:LEAVE_OK:NONE",
                    "1529938978925:LEAVING:LEFT_SELF:LEAVING",
                    "1529938978921:MASTER:LEAVE_REQ:LEAVING",
                    "1529938970805:CHECKING_SLAVES:GETVERS_OK:MASTER",
                    "1529938970798:CHECKING_SLAVES:GETVERS_OK:CHECKING_SLAVES",
                    "1529938970777:LISTING:LIST_OK:CHECKING_SLAVES",
                    "1529938970777:WATCHING:EXISTS_OK:LISTING",
                    "1529938970777:CREATING:CREATE_OK:WATCHING",
                    "1529938970775:PEERING:GETPEERS_DONE:CREATING",
                    "1529938970775:NONE:NONE:PEERING"
                ],
                "master": {
                    "id": null,
                    "url": null
                },
                "peers": [
                    "127.0.0.1:6020",
                    "127.0.0.3:6025"
                ]
            },
            "status": {
                "message": "OK",
                "status": 200
            }
        },
        "127.0.0.2:6024": {
            "body": null,
            "status": {
                "message": "OK",
                "status": 200
            }
        },
        "127.0.0.3:6025": {
            "body": {
                "#": {
                    "getvers": 0,
                    "pipefrom": 0,
                    "refcount": 2
                },
                "base": {
                    "name": "E11A2CF2E8001309E9500E644836C8F050A0BB9CD39F10276B44AD30B4AABC99.1",
                    "type": "meta2",
                    "zk": "7353556D83E9E1F88E851072150B0B87DB537C128E2271CC4E8F014051EB9B28"
                },
                "local": {
                    "id": null,
                    "state": "NONE",
                    "url": "127.0.0.3:6025"
                },
                "log": [
                    "1529938978925:LEAVING:LEAVE_OK:NONE",
                    "1529938978925:LEAVING:LEFT_SELF:LEAVING",
                    "1529938978925:LEAVING:LEFT_MASTER:LEAVING",
                    "1529938978923:SLAVE:LEAVE_REQ:LEAVING",
                    "1529938970877:CHECKING_MASTER:GETVERS_OK:SLAVE",
                    "1529938970852:ASKING:MASTER_OK:CHECKING_MASTER",
                    "1529938970843:LISTING:LIST_OK:ASKING",
                    "1529938970843:WATCHING:EXISTS_OK:LISTING",
                    "1529938970831:CREATING:CREATE_OK:WATCHING",
                    "1529938970826:PEERING:GETPEERS_DONE:CREATING",
                    "1529938970801:NONE:NONE:PEERING"
                ],
                "master": {
                    "id": null,
                    "url": null
                },
                "peers": [
                    "127.0.0.1:6020",
                    "127.0.0.1:6023"
                ]
            },
            "status": {
                "message": "OK",
                "status": 200
            }
        }
    }


Update container
++++++++++++++++

::

    $ openio container set $CNT --property rebuild=$(date +%s)


Check state of election
+++++++++++++++++++++++

Any reference of old peer must be absent

::

    $ curl -XPOST 'http://127.0.0.1:6000/v3.0/$NS/admin/debug?acct=murlock&ref=cnt2&type=meta2' | python -m json.tool
    {
        "127.0.0.1:6023": {
            "body": {
                "#": {
                    "getvers": 0,
                    "pipefrom": 0,
                    "refcount": 2
                },
                "base": {
                    "name": "E11A2CF2E8001309E9500E644836C8F050A0BB9CD39F10276B44AD30B4AABC99.1",
                    "type": "meta2",
                    "zk": "7353556D83E9E1F88E851072150B0B87DB537C128E2271CC4E8F014051EB9B28"
                },
                "local": {
                    "id": 296,
                    "state": "MASTER",
                    "url": "127.0.0.1:6023"
                },
                "log": [
                    "1529938987164:CHECKING_SLAVES:GETVERS_OK:MASTER",
                    "1529938987160:CHECKING_SLAVES:GETVERS_OK:CHECKING_SLAVES",
                    "1529938987156:LISTING:LIST_OK:CHECKING_SLAVES",
                    "1529938987155:SLAVE:LEFT_MASTER:LISTING",
                    "1529938987152:CHECKING_MASTER:GETVERS_OK:SLAVE",
                    "1529938987119:ASKING:MASTER_OK:CHECKING_MASTER",
                    "1529938987119:LISTING:LIST_OK:ASKING",
                    "1529938987118:WATCHING:EXISTS_OK:LISTING",
                    "1529938987113:CREATING:CREATE_OK:WATCHING",
                    "1529938987108:PEERING:GETPEERS_DONE:CREATING",
                    "1529938987106:NONE:NONE:PEERING",
                    "1529938978925:LEAVING:LEAVE_OK:NONE",
                    "1529938978925:LEAVING:LEFT_SELF:LEAVING",
                    "1529938978921:MASTER:LEAVE_REQ:LEAVING",
                    "1529938970805:CHECKING_SLAVES:GETVERS_OK:MASTER",
                    "1529938970798:CHECKING_SLAVES:GETVERS_OK:CHECKING_SLAVES",
                    "1529938970777:LISTING:LIST_OK:CHECKING_SLAVES",
                    "1529938970777:WATCHING:EXISTS_OK:LISTING",
                    "1529938970777:CREATING:CREATE_OK:WATCHING",
                    "1529938970775:PEERING:GETPEERS_DONE:CREATING",
                    "1529938970775:NONE:NONE:PEERING"
                ],
                "master": {
                    "id": 296,
                    "url": null
                },
                "peers": [
                    "127.0.0.3:6025",
                    "127.0.0.2:6024"
                ]
            },
            "status": {
                "message": "OK",
                "status": 200
            }
        },
        "127.0.0.2:6024": {
            "body": {
                "#": {
                    "getvers": 0,
                    "pipefrom": 0,
                    "refcount": 3
                },
                "base": {
                    "name": "E11A2CF2E8001309E9500E644836C8F050A0BB9CD39F10276B44AD30B4AABC99.1",
                    "type": "meta2",
                    "zk": "7353556D83E9E1F88E851072150B0B87DB537C128E2271CC4E8F014051EB9B28"
                },
                "local": {
                    "id": 298,
                    "state": "SLAVE",
                    "url": "127.0.0.2:6024"
                },
                "log": [
                    "1529938987179:SYNCING:SYNC_OK:SLAVE",
                    "1529938987165:CHECKING_MASTER:GETVERS_OLD:SYNCING",
                    "1529938987158:ASKING:MASTER_OK:CHECKING_MASTER",
                    "1529938987157:LISTING:LIST_OK:ASKING",
                    "1529938987157:WATCHING:EXISTS_OK:LISTING",
                    "1529938987157:CREATING:CREATE_OK:WATCHING",
                    "1529938987155:PEERING:GETPEERS_DONE:CREATING",
                    "1529938987155:NONE:NONE:PEERING",
                    "1529938987155:LEAVING:LEAVE_OK:NONE",
                    "1529938987155:LEAVING:LEFT_SELF:LEAVING",
                    "1529938987154:CHECKING_SLAVES:GETVERS_OLD:LEAVING",
                    "1529938987150:CHECKING_SLAVES:GETVERS_OLD:CHECKING_SLAVES",
                    "1529938987128:LISTING:LIST_OK:CHECKING_SLAVES",
                    "1529938987119:WATCHING:EXISTS_OK:LISTING",
                    "1529938987118:CREATING:CREATE_OK:WATCHING",
                    "1529938987105:PEERING:GETPEERS_DONE:CREATING",
                    "1529938987105:NONE:NONE:PEERING"
                ],
                "master": {
                    "id": 296,
                    "url": "127.0.0.1:6023"
                },
                "peers": [
                    "127.0.0.1:6023",
                    "127.0.0.3:6025"
                ]
            },
            "status": {
                "message": "OK",
                "status": 200
            }
        },
        "127.0.0.3:6025": {
            "body": {
                "#": {
                    "getvers": 0,
                    "pipefrom": 0,
                    "refcount": 2
                },
                "base": {
                    "name": "E11A2CF2E8001309E9500E644836C8F050A0BB9CD39F10276B44AD30B4AABC99.1",
                    "type": "meta2",
                    "zk": "7353556D83E9E1F88E851072150B0B87DB537C128E2271CC4E8F014051EB9B28"
                },
                "local": {
                    "id": 297,
                    "state": "SLAVE",
                    "url": "127.0.0.3:6025"
                },
                "log": [
                    "1529938987159:CHECKING_MASTER:GETVERS_OK:SLAVE",
                    "1529938987156:ASKING:MASTER_OK:CHECKING_MASTER",
                    "1529938987156:LISTING:LIST_OK:ASKING",
                    "1529938987155:SLAVE:LEFT_MASTER:LISTING",
                    "1529938987151:CHECKING_MASTER:GETVERS_OK:SLAVE",
                    "1529938987124:ASKING:MASTER_OK:CHECKING_MASTER",
                    "1529938987124:LISTING:LIST_OK:ASKING",
                    "1529938987119:WATCHING:EXISTS_OK:LISTING",
                    "1529938987117:CREATING:CREATE_OK:WATCHING",
                    "1529938987115:PEERING:GETPEERS_DONE:CREATING",
                    "1529938987114:NONE:NONE:PEERING",
                    "1529938978925:LEAVING:LEAVE_OK:NONE",
                    "1529938978925:LEAVING:LEFT_SELF:LEAVING",
                    "1529938978925:LEAVING:LEFT_MASTER:LEAVING",
                    "1529938978923:SLAVE:LEAVE_REQ:LEAVING",
                    "1529938970877:CHECKING_MASTER:GETVERS_OK:SLAVE",
                    "1529938970852:ASKING:MASTER_OK:CHECKING_MASTER",
                    "1529938970843:LISTING:LIST_OK:ASKING",
                    "1529938970843:WATCHING:EXISTS_OK:LISTING",
                    "1529938970831:CREATING:CREATE_OK:WATCHING",
                    "1529938970826:PEERING:GETPEERS_DONE:CREATING",
                    "1529938970801:NONE:NONE:PEERING"
                ],
                "master": {
                    "id": 296,
                    "url": "127.0.0.1:6023"
                },
                "peers": [
                    "127.0.0.1:6023",
                    "127.0.0.2:6024"
                ]
            },
            "status": {
                "message": "OK",
                "status": 200
            }
        }
    }

