.. title:: Learn OpenIO SDS the hard way, your Swift/S3 on premise backend built from scratch.

.. _ref-build-from-source:

=================
Build from Source
=================

.. contents::
   :backlinks: none
   :depth: 1
   :local:

This section describes how to compile OpenIO SDS from the official source downloaded from GitHub.

The build procedure is available for **Ubuntu 16.04**.

Set the $SDS variable
---------------------
Throughout this guide, the environment variable `SDS` will be used several times. You should ensure this variable is always defined.
It should be set to the name of directory where you are building OpenIO SDS.

   .. code-block:: shell

      export SDS=$HOME/local


Configure Repository
--------------------
We provide easy access to build and runtime dependency versions not available in common distributions.

   .. code-block:: shell

      echo "deb {{UBUNTU_REPO_DEB}}" | sudo tee /etc/apt/sources.list.d/openio-sds.list
      curl http://mirror.openio.io/pub/repo/openio/APT-GPG-KEY-OPENIO-0 | sudo apt-key add -
      sudo apt-get -y update


Build Dependencies
------------------
Build tools

   .. code-block:: shell

      sudo apt-get -y install git cmake

Build dependencies

   .. code-block:: shell

      sudo apt-get -y install \
          flex bison \
          libcurl4-gnutls-dev \
          libglib2.0-dev \
          libapreq2-dev \
          libsqlite3-dev \
          libjson-c-dev \
          apache2 \
          apache2-dev \
          liblzo2-dev \
          libzmq3-dev \
          libattr1-dev \
          libzookeeper-mt-dev \
          openio-asn1c \
          openio-gridinit \
          liberasurecode-dev \
          python-dev \
          python-pbr \
          python-setuptools \
          libleveldb-dev

Download Source Code
--------------------

The official OpenIO SDS source code is available from Github.

   .. code-block:: shell

      git clone https://github.com/open-io/oio-sds.git -b {{OIO_SDS_BRANCHNAME}}


Build
-----

Perform the build in a separate folder from sources.

   .. code-block:: shell

      mkdir build && cd build
      cmake \
          -DCMAKE_INSTALL_PREFIX=${SDS} \
          -DLD_LIBDIR=lib \
          -DAPACHE2_MODDIR=${SDS}/lib/apache2 \
          -DAPACHE2_LIBDIR=/usr/lib/apache2 \
          -DAPACHE2_INCDIR=/usr/include/apache2 \
          ../oio-sds
      make

Install
-------

   .. code-block:: shell

      make install
      ( cd ../oio-sds && python setup.py install --user --install-scripts=${SDS}/bin)

Binaries and scripts are installed in ``$SDS/bin``. Libraries are installed in ``$SDS/lib``.
Note that for Python, output is in local user installation ``$HOME/.local/``.

Sandbox Setup
-------------


Environment
^^^^^^^^^^^

Set a few environment variables so everything we built previously is correctly found and used.

   .. code-block:: shell

      echo "export PATH=${PATH}:$SDS/bin" >> $HOME/.bashrc
      echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$SDS/lib" >> $HOME/.bashrc
      source $HOME/.bashrc


Runtime Dependencies
^^^^^^^^^^^^^^^^^^^^

To run the sandbox, you need additional runtime dependencies:

External services:

* Redis: advanced key-value store used by account services.

* Beanstalkd: simple and fast work queue used by OpenIO to run background jobs.

Libraries:

* Python dependencies: several services and tools in OpenIO are built with Python


   .. code-block:: shell

      sudo apt-get install -y
          python-cliff \
          python-eventlet \
          python-gunicorn \
          python-plyvel \
          python-redis \
          python-requests \
          python-werkzeug \
          python-xattr \
          python-yaml \
          python-zookeeper \
          redis-server \
          beanstalkd

We used to start redis from systemctl, but an instance will be started along with
OpenIO SDS services.

Create Sandbox
^^^^^^^^^^^^^^

   .. code-block:: shell

      oio-reset.sh -f etc/bootstrap-preset-MINIMAL.yml
