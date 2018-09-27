============
Rawx Service
============

Description
-----------

Prerequisites
-------------

Installation
------------

Configuration
-------------

Sample configuration file
-------------------------

.. code-block:: shell
   :caption: /etc/oio/sds/OPENIO/rawx-0/rawx-0-httpd.conf

   LoadModule mpm_worker_module   /usr/lib/apache2/modules/mod_mpm_worker.so
   LoadModule authz_core_module   /usr/lib/apache2/modules/mod_authz_core.so
   LoadModule dav_module          /usr/lib/apache2/modules/mod_dav.so
   LoadModule mime_module         /usr/lib/apache2/modules/mod_mime.so
   LoadModule dav_rawx_module     /usr/lib/apache2/modules/mod_dav_rawx.so
   LoadModule setenvif_module     /usr/lib/apache2/modules/mod_setenvif.so
   LoadModule alias_module        /usr/lib/apache2/modules/mod_alias.so
   LoadModule env_module          /usr/lib/apache2/modules/mod_env.so

   Alias / /x/

   Listen          172.17.0.2:6201
   PidFile         /run/oio/sds/OPENIO-rawx-0-httpd.pid
   ServerRoot      /var/lib/oio/sds/OPENIO/coredump
   ServerName      localhost
   ServerSignature Off
   ServerTokens    Prod
   DocumentRoot    /var/lib/oio/sds/OPENIO/rawx-0
   TypesConfig     /etc/mime.types

   User  openio
   Group openio

   SetEnv INFO_SERVICES OIO,OPENIO,rawx,1
   SetEnv LOG_TYPE access
   SetEnv LEVEL INF
   SetEnv HOSTNAME node1.openstacklocal

   SetEnvIf Remote_Addr "^" log-cid-out=1
   SetEnvIf Remote_Addr "^" log-cid-in=0
   SetEnvIf Request_Method "PUT" log-cid-in=1
   SetEnvIf Request_Method "PUT" !log-cid-out
   SetEnvIf log-cid-in 0 !log-cid-in

   LogFormat "%{%b %d %T}t %{HOSTNAME}e %{INFO_SERVICES}e %{pid}P %{tid}P %{LOG_TYPE}e %{LEVEL}e %{Host}i %a:%{remote}p %m %>s %D %I %{x-oio-chunk-meta-container-id}i %{x-oio-req-id}i %U" log/cid-in
   LogFormat "%{%b %d %T}t %{HOSTNAME}e %{INFO_SERVICES}e %{pid}P %{tid}P %{LOG_TYPE}e %{LEVEL}e %{Host}i %a:%{remote}p %m %>s %D %O %{x-oio-chunk-meta-container-id}o %{x-oio-req-id}i %U" log/cid-out

   ErrorLog /var/log/oio/sds/OPENIO/rawx-0/rawx-0-httpd-errors.log
   SetEnvIf Request_URI "/(stat|info)$" nolog=1

   SetEnvIf nolog 1 !log-cid-out
   SetEnvIf nolog 1 !log-cid-in

   CustomLog /var/log/oio/sds/OPENIO/rawx-0/rawx-0-httpd-access.log log/cid-out env=log-cid-out
   CustomLog /var/log/oio/sds/OPENIO/rawx-0/rawx-0-httpd-access.log log/cid-in  env=log-cid-in

   <IfModule worker.c>
   MaxRequestsPerChild 0
   MaxSpareThreads 256
   MinSpareThreads 32
   ServerLimit 16
   StartServers 1
   ThreadsPerChild 256
   </IfModule>


   DavDepthInfinity Off

   grid_docroot    /var/lib/oio/sds/OPENIO/rawx-0
   # How many hexdigits must be used to name the indirection directories
   grid_hash_width 3
   # How many levels of directories are used to store chunks
   grid_hash_depth 1
   # At the end of an upload, perform a fsync() on the chunk file itself
   grid_fsync      enabled
   # At the end of an upload, perform a fsync() on the directory holding the chunk
   grid_fsync_dir  enabled
   # Preallocate space for the chunk file (enabled by default)
   #grid_fallocate enabled
   # Enable compression ('zlib' or 'lzo' or 'off')
   grid_compression off
   grid_namespace  OPENIO
   grid_dir_run    /run/oio/sds

   <Directory />
   DAV rawx
   AllowOverride None
   Require all granted
   Options -SymLinksIfOwnerMatch -FollowSymLinks -Includes -Indexes
   </Directory>

   <VirtualHost 172.17.0.2:6201>
   # DO NOT REMOVE (even if empty) !
   </VirtualHost>
