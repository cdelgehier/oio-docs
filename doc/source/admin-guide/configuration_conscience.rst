===================
Conscience Services
===================

Description
-----------

Conscience services are composed of a conscience service and conscience-agent services.

Prerequisites
-------------

Installation
------------

Configuration
-------------

Persistent conscience service status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use Case
^^^^^^^^
You can specify an option to add persistence for conscience service status.

The goal of this persistence is to unlock known services before restarting conscience,
making openio cluster unlockall unnecessary. New services added while conscience is
stopped still requires a manual unlock operation.


Enable persistence
^^^^^^^^^^^^^^^^^^
You must specify the file path to use for persistence. Services status is written in this file
and conscience reads it at restart to know which services were enabled before conscience was stopped.

You can get the conscience status using ``gridinit_cmd status2 @conscience``.

To enable persistence at launch:

  .. code-block:: console

     # oio-daemon <conscience configuration path> -O PersistencePath=<persistence file path>

Statuses are written every 30 seconds by default, but you can change this value
with the option ```-O PersistencePeriod=N`` where N is the period in seconds.

Sample configuration file
-------------------------

.. code-block:: ini
   :caption: /etc/oio/sds/OPENIO/conscience-0/conscience-0.conf

   [General]
   # Timeout on read operations
   to_op=1000
   # Timeout on accepting connections
   to_cnx=1000

   flag.NOLINGER=true
   flag.SHUTDOWN=false
   flag.KEEPALIVE=false
   flag.QUICKACK=false

   [Server.conscience]
   min_workers=2
   min_spare_workers=2
   max_spare_workers=10
   max_workers=10
   listen=172.17.0.5:6000
   plugins=conscience,stats,ping,fallback

   [Service]
   namespace=OPENIO
   type=conscience
   register=false
   load_ns_info=false

   [Plugin.conscience]
   param_storage_conf=/etc/oio/sds/OPENIO/conscience-0/conscience-0-policies.conf
   path=/usr/lib64/grid/msg_conscience.so
   param_service_conf=/etc/oio/sds/OPENIO/conscience-0/conscience-0-services.conf
   param_namespace=OPENIO

   [Plugin.stats]
   path=/usr/lib64/grid/msg_stats.so

   [Plugin.ping]
   path=/usr/lib64/grid/msg_ping.so

   [Plugin.fallback]
   path=/usr/lib64/grid/msg_fallback.so


   # Multi-conscience
   #param_hub.me=tcp://172.17.0.5:18000
   #param_hub.group=tcp://172.17.0.3:18000,tcp://172.17.0.4:18000


.. code-block:: ini
   :caption: /etc/oio/sds/OPENIO/conscience-0/conscience-0-policies.conf

   [STORAGE_POLICY]
   # Storage policy definitions
   # ---------------------------
   #
   # The first word is the service pool to use,
   # the second word is the data security to use.
   ERASURECODE=NONE: ERASURECODE
   ECLIBEC144D1=NONE: ECLIBEC144D1
   ECISAL144D1=NONE: ECISAL144D1
   SINGLE=NONE: NONE
   THREECOPIES=NONE: DUPONETHREE
   ECISAL63D1=NONE: ECISAL63D1
   ECLIBEC63D1=NONE: ECLIBEC63D1
   TWOCOPIES=NONE: DUPONETWO

   [DATA_SECURITY]
   # Data security definitions
   # --------------------------
   #
   # The first word is the kind of data security ("plain", "ec" or "backblaze"),
   # after the '/' are the parameters of the data security.
   # List of possible values for the "algo" parameter of "ec" data security:
   # "jerasure_rs_vand"       EC_BACKEND_JERASURE_RS_VAND
   # "jerasure_rs_cauchy"     EC_BACKEND_JERASURE_RS_CAUCHY
   # "flat_xor_hd"            EC_BACKEND_FLAT_XOR_HD
   # "isa_l_rs_vand"          EC_BACKEND_ISA_L_RS_VAND
   # "shss"                   EC_BACKEND_SHSS
   # "liberasurecode_rs_vand" EC_BACKEND_LIBERASURECODE_RS_VAND
   ERASURECODE=ec/k=6,m=3,algo=liberasurecode_rs_vand,distance=1
   DUPONETHREE=plain/distance=1,nb_copy=3
   ECLIBEC144D1=ec/k=14,m=4,algo=liberasurecode_rs_vand,distance=1
   ECISAL144D1=ec/k=14,m=4,algo=isa_l_rs_vand,distance=1
   ECLIBEC123D1=ec/k=12,m=3,algo=liberasurecode_rs_vand,distance=1
   DUPONETWO=plain/distance=1,nb_copy=2
   ECISAL63D1=ec/k=6,m=3,algo=isa_l_rs_vand,distance=1
   ECLIBEC63D1=ec/k=6,m=3,algo=liberasurecode_rs_vand,distance=1
   ECISAL123D1=ec/k=12,m=3,algo=isa_l_rs_vand,distance=1


.. code-block:: ini
   :caption: /etc/oio/sds/OPENIO/conscience-0/conscience-0-services.conf

   # Service pools declarations
   # ----------------------------
   #
   # Pools are automatically created if not defined in configuration,
   # according to storage policy or service update policy rules.
   #
   # "targets" is a ';'-separated list.
   # Each target is a ','-separated list of:
   # - the number of services to pick,
   # - the name of a slot where to pick the services,
   # - the name of a slot where to pick services if there is
   #   not enough in the previous slot
   # - and so on...
   #
   # "nearby_mode" is a boolean telling to find services close to each other
   # instead of far from each other.
   #
   #### power user options, don't set them unless you know what you are doing!
   # "mask" is a 64 bits hexadecimal mask used to check service distance.
   # It defaults to FFFFFFFFFFFF0000. It can also be specified as "/48".
   #
   # "mask_max_shift" is the maximum number of bits to shift the mask
   # to degrade it when distance requirement are not satisfiable.
   # It defaults to 16.
   #

   #[pool:rawx21]
   #targets=2,rawx-europe,rawx;1,rawx-asia,rawx;
   #min_dist=2


   # Service types declarations
   # ---------------------------

   [type:sqlx]
   score_expr=((num stat.space)>=5) * root(3,(((num stat.cpu)+1)*(num stat.space)*((num stat.io)+1)))
   score_timeout=120

   [type:account]
   score_expr=(num tag.up) * ((num stat.cpu)+1)
   score_timeout=120

   [type:rawx]
   score_expr=(num tag.up) * ((num stat.space)>=5) * root(3,(((num stat.cpu)+1)*(num stat.space)*((num stat.io)+1)))
   score_timeout=120

   [type:rdir]
   score_expr=(num tag.up) * ((num stat.cpu)+1) * ((num stat.space)>=2)
   score_timeout=120

   [type:redis]
   score_expr=(num tag.up) * ((num stat.cpu)+1)
   score_timeout=120

   [type:meta0]
   score_expr=root(2,((num stat.cpu) * ((num stat.io)+1)))
   score_timeout=3600

   [type:meta1]
   score_expr=((num stat.space)>=5) * root(3,(((num stat.cpu)+1)*(num stat.space)*((num stat.io)+1)))
   score_timeout=120

   [type:meta2]
   score_expr=((num stat.space)>=5) * root(3,(((num stat.cpu)+1)*(num stat.space)*((num stat.io)+1)))
   score_timeout=120

   [type:oiofs]
   score_expr=((num stat.cpu)+1)
   score_timeout=120


.. code-block:: yaml
   :caption: /etc/oio/sds/OPENIO/account-0/account-0.conf

   # Namespace name
   namespace: OPENIO
   # Run daemon as user
   user: openio
   #
   # Logging configuration
   log_level: info
   log_facility: LOG_LOCAL0
   log_address: /dev/log
   syslog_prefix: OIO,OPENIO,conscienceagent,1
   #
   # Include path for services conf
   # # example service is provided in service-watch.yml
   include_dir: /etc/oio/sds/OPENIO/watch
   #
   #
   # Global checks configuration
   # Check interval (in seconds)
   check_interval: 5
   # Rise (number of consecutive successful checks to switch service status to up)
   rise: 1
   # Fall (number of consecutive unsuccessful checks to switch service status to down)
   fall: 2
