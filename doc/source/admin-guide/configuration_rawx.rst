========================
Configure a rawx service
========================

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

.. code-block:: text

   LoadModule mpm_worker_module /usr/lib/apache2/modules/mod_mpm_worker.so
   LoadModule authz_core_module /usr/lib/apache2/modules/mod_authz_core.so
   LoadModule setenvif_module /usr/lib/apache2/modules/mod_setenvif.so
   LoadModule env_module /usr/lib/apache2/modules/mod_env.so
   LoadModule dav_module /usr/lib/apache2/modules/mod_dav.so
   LoadModule mime_module /usr/lib/apache2/modules/mod_mime.so
   LoadModule alias_module /usr/lib/apache2/modules/mod_alias.so
   LoadModule dav_rawx_module /path/to/install/of/apache2/module/mod_dav_rawx.so
   
   <IfModule !mod_logio.c>
     LoadModule logio_module /usr/lib/apache2/modules/mod_logio.so
   </IfModule>
   <IfModule !unixd_module>
     LoadModule unixd_module /usr/lib/apache2/modules/mod_unixd.so
   </IfModule>
   <IfModule !log_config_module>
     LoadModule log_config_module /usr/lib/apache2/modules/mod_log_config.so
   </IfModule>
   
   Listen 127.0.0.4:6034
   PidFile /home/jfs/.oio/sds/run/OPENIO-rawx-1.pid
   ServerRoot /tmp
   ServerName 127.0.0.4
   ServerSignature Off
   ServerTokens Prod
   DocumentRoot /home/jfs/.oio/sds/run
   TypesConfig /etc/mime.types
   
   User  jfs
   Group jfs
   
   SetEnv INFO_SERVICES OIO,OPENIO,rawx,1
   SetEnv LOG_TYPE access
   SetEnv LEVEL INF
   SetEnv HOSTNAME oio
   
   SetEnvIf Remote_Addr "^" log-cid-out=1
   SetEnvIf Remote_Addr "^" log-cid-in=0
   SetEnvIf Request_Method "PUT" log-cid-in=1
   SetEnvIf Request_Method "PUT" !log-cid-out
   SetEnvIf log-cid-in 0 !log-cid-in
   
   LogFormat "%{%b %d %T}t %{HOSTNAME}e %{INFO_SERVICES}e %{pid}P %{tid}P %{LOG_TYPE}e %{LEVEL}e %{Host}i %a:%{remote}p %m %>s %D %O %{x-oio-chunk-meta-container-id}i %{x-oio-req-id}i %U" log/cid-in
   LogFormat "%{%b %d %T}t %{HOSTNAME}e %{INFO_SERVICES}e %{pid}P %{tid}P %{LOG_TYPE}e %{LEVEL}e %{Host}i %a:%{remote}p %m %>s %D %O %{x-oio-chunk-meta-container-id}o %{x-oio-req-id}i %U" log/cid-out
   
   #ErrorLog /home/jfs/.oio/sds/logs/OPENIO-rawx-1-errors.log
   ErrorLog "| /usr/bin/logger -t OPENIO-rawx-1"
   SetEnvIf Request_URI "/(stat|info)$" nolog=1
   
   SetEnvIf nolog 1 !log-cid-out
   SetEnvIf nolog 1 !log-cid-in
   
   #CustomLog /home/jfs/.oio/sds/logs/OPENIO-rawx-1-access.log log/cid-out env=log-cid-out
   #CustomLog /home/jfs/.oio/sds/logs/OPENIO-rawx-1-access.log log/cid-in  env=log-cid-in
   CustomLog "| /usr/bin/logger -t OPENIO-rawx-1" log/cid-in  env=log-cid-in
   LogLevel info
   
   <IfModule prefork.c>
   StartServers 5
   MaxClients 40
   MinSpareServers 2
   MaxSpareServers 40
   </IfModule>
   
   <IfModule worker.c>
   MaxClients 512
   MaxRequestWorkers 512
   ThreadsPerChild 256
   StartServers 1
   MinSpareThreads 8
   MaxSpareThreads 32
   MaxRequestsPerChild 0
   </IfModule>
   
   DavDepthInfinity Off
   
   grid_docroot           /home/jfs/.oio/sds/data/OPENIO-rawx-1
   grid_namespace         OPENIO
   grid_dir_run           /home/jfs/.oio/sds/run
   #grid_service_id        ${SERVICE_ID}
   
   # How many hexdigits must be used to name the indirection directories
   grid_hash_width        3
   
   # How many levels of directories are used to store chunks.
   grid_hash_depth        1
   
   # At the end of an upload, perform a fsync() on the chunk file itself
   grid_fsync             disabled
   
   # At the end of an upload, perform a fsync() on the directory holding the chunk
   grid_fsync_dir         disabled
   
   # Preallocate space for the chunk file (enabled by default)
   #grid_fallocate enabled
   
   # Triggers Access Control List (acl)
   # DO NOT USE, this is broken
   #grid_acl disabled
   
   # Enable compression ('zlib' or 'lzo' or 'off')
   grid_compression off
   
   Alias / /x/
   
   <Directory />
   DAV rawx
   AllowOverride None
   Require all granted
   Options -SymLinksIfOwnerMatch -FollowSymLinks -Includes -Indexes
   </Directory>
   
   <VirtualHost 127.0.0.4:6034>
   # DO NOT REMOVE (even if empty) !
   </VirtualHost>

