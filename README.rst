OpenIO Docs
+++++++++++

This repository contains documentation for the OpenIO project.

It includes these manuals:

 * Installation Guide
 * Installation Guide for Swift/S3
 * Project Guide
 * User Guide
 * CLI Guide
 * Docker Image Guide


Building
========
There are several manuals in the ``doc/`` directory/

Guides
======
Guides are in RST format. We use tox to prepare and build all guides::

        tox

The generated HTML documentations can be found at::

        result-docs/
