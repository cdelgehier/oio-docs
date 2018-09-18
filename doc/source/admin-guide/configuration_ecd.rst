========================
Configure an ECD Service
========================

Description
-----------

ECD (Erasure Coding Daemon) is used to manage Erasure Coding through C and Java SDKs.

Prerequisites
-------------

Installation
------------

Configuration
-------------

Sample configuration file
-------------------------

.. code-block:: shell
   :caption: /etc/oio/sds/OPENIO/ecd-0/ecd-0-httpd.conf

   LoadModule mpm_worker_module   /usr/lib64/httpd/modules/mod_mpm_worker.so
   LoadModule authz_core_module   /usr/lib64/httpd/modules/mod_authz_core.so
   LoadModule wsgi_module         /usr/lib64/httpd/modules/mod_wsgi.so
   LoadModule unixd_module        /usr/lib64/httpd/modules/mod_unixd.so
   LoadModule log_config_module   /usr/lib64/httpd/modules/mod_log_config.so

   Listen          172.17.0.6:6017
   PidFile         /run/ecd/OPENIO/ecd-0/httpd.pid
   ServerRoot      /var/lib/oio/sds/OPENIO/coredump
   ServerName      localhost
   ServerSignature off
   ServerTokens    Prod
   DocumentRoot    /var/lib/oio/sds/OPENIO/ecd-0

   User  openio
   Group openio

   LogFormat "%h %l %t \"%r\" %>s %b %D" log/common
   ErrorLog  /var/log/oio/sds/OPENIO/ecd-0/ecd-0-httpd-errors.log
   CustomLog /var/log/oio/sds/OPENIO/ecd-0/ecd-0-httpd-access.log log/common env=!dontlog
   LogLevel  info

   <IfModule setenvif_module>
   SetEnvIf Request_URI "^/(info|stat)$" dontlog
   </IfModule>

   <IfModule wsgi_module>
   WSGIDaemonProcess ecd-0 processes=4 threads=1 user=openio group=openio
   WSGIApplicationGroup ecd-0
   WSGIScriptAlias / /etc/oio/sds/OPENIO/ecd-0/ecd-0.wsgi
   WSGISocketPrefix /run/ecd/OPENIO/ecd-0
   WSGIChunkedRequest On
   </IfModule>

   <IfModule worker.c>
   StartServers        5
   MaxClients          100
   MinSpareThreads     5
   MaxSpareThreads     25
   ThreadsPerChild     10
   MaxRequestsPerChild 0
   </IfModule>

   LimitRequestFields 200

   <VirtualHost 172.17.0.6:6017>
   # DO NOT REMOVE (even if empty) !
   </VirtualHost>
