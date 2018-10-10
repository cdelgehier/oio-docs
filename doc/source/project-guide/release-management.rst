.. title:: OpenIO release cycle management, semantic versioning.

==================
Release Management
==================

Version numbers
---------------

Either from the Open Source side (oio-sds_, gridinit_, etc.) or the close
source part (:ref:`label-oiofs-architecture`, :ref:`label-replicator-value`,
:ref:`label-oiobilling-value`, etc), each OpenIO subproject has its own
version number. We will follow the rules defined in
`Openstack's fork of Semantic Versioning`_.

* Breaking changes increment the major version number,
* Regular changes increment the minor version number,
* Bug fixes will increment the patch version number.

A branch in the source code repository should be created for each long-term
supported version, named like *release-X.Y*, with X and Y being the major
and minor version numbers.

OpenIO distributions (aka software suites)
------------------------------------------

From time to time, we release a **distribution** in the form
of a package repository (RPM and DEB) containing coherent versions of all
subprojects. These distributions are named after the year and
the month they are released (e.g. 16.04 for April 2016), as does Ubuntu.
During its life, a distribution will receive only non-breaking updates
of its subprojects.

.. _oio-sds: https://github.com/open-io/oio-sds
.. _gridinit: https://github.com/open-io/gridinit
.. _Openstack's fork of Semantic Versioning: http://docs.openstack.org/developer/pbr/semver.html
