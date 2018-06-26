=========================
Rebalance a volume: meta1
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
    export CNT=cnt3

    export OLDMETA1=127.0.0.1:6013


Retrieve information
++++++++++++++++++++

::

    $ openio container locate $CNT
    +-----------+--------------------------------------------------------------------+
    | Field     | Value                                                              |
    +-----------+--------------------------------------------------------------------+
    | account   | murlock                                                            |
    | base_name | D10F6AFAF447A6F1BDF855CD8EDBC754F7AD76189B17102A5FB0E96049CD0895.1 |
    | meta0     | 127.0.0.1:6010, 127.0.0.3:6012, 127.0.0.2:6011                     |
    | meta1     | 127.0.0.1:6013, 127.0.0.2:6017, 127.0.0.3:6018                     |
    | meta2     | 127.0.0.1:6026, 127.0.0.2:6024, 127.0.0.1:6023                     |
    | name      | cnt3                                                               |
    +-----------+--------------------------------------------------------------------+
    $ export META1="127.0.0.2 127.0.0.3"


Update meta0 for prefix D10F
++++++++++++++++++++++++++++

Note: prefix size depends on your configuration

::

    $ export pfx=D10F
    # choose a new meta1 server
    $ NEWMETA1=$(sqlite3 OPENIO.meta0 "select addr from meta1 where addr not in (select addr from meta1 where hex(prefix) = '$pfx') order by random() limit 1")
    $ echo $NEWMETA1
    127.0.0.2:6014
    # update prefix on ALL meta0
    $ for ip in $(openio cluster list meta0 -f value -c Id | cut -f1 -d:); do
        ssh $ip find /var/openio -name OPENIO.meta0 -exec sqlite3 \{\} "update meta1 set addr='$NEWMETA1' where addr='$OLDMETA1' and hex(prefix) = '$pfx'" \;
    done

Update meta1 peers
++++++++++++++++++

::

    $ PEERS=$(sqlite3 OPENIO.meta0 "select addr from meta1 where hex(prefix) = '$pfx';" | tr '\n' ',' | cut -f1-3 -d,)
    $ echo $PEERS
    127.0.0.2:6014,127.0.0.2:6017,127.0.0.3:6018
    $ for ip in $META1; do
        ssh $ip find /var/openio -iname $pfx.meta1 -exec sqlite3 \{\} "update admin set v='$PEERS' where k='sys.peers'" \;
    done


Restart meta0 and meta1
+++++++++++++++++++++++

::

    gridinit_cmd restart @meta0 @meta1


Check container locate
++++++++++++++++++++++

::

    $ openio container locate $CNT
    +-----------+--------------------------------------------------------------------+
    | Field     | Value                                                              |
    +-----------+--------------------------------------------------------------------+
    | account   | murlock                                                            |
    | base_name | D10F6AFAF447A6F1BDF855CD8EDBC754F7AD76189B17102A5FB0E96049CD0895.1 |
    | meta0     | 127.0.0.1:6010, 127.0.0.3:6012, 127.0.0.2:6011                     |
    | meta1     | 127.0.0.2:6014, 127.0.0.2:6017, 127.0.0.3:6018                     |
    | meta2     | 127.0.0.1:6026, 127.0.0.2:6024, 127.0.0.1:6023                     |
    | name      | cnt3                                                               |
    +-----------+--------------------------------------------------------------------+

