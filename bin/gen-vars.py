#!/usr/bin/env python
# coding: utf8
"""
Expose all compoments from from doc/components.json to
environment variables:
For example, oio-sds will be exposed as:
    OIO_SDS_BRANCHNAME=4.1.4
    OIO_SDS_REPOSITORY=http://github.com/open-io/oio-sds
"""

from __future__ import print_function
import json
import re
import sys

ASCII = re.compile(r'^[A-Z0-9_]*$')


def conv(field):
    field = field.upper()
    field = field.replace("-", "_")
    assert ASCII.match(field), "unexpected variable name: " + field
    return field


def main(out):
    data = None
    with open("components.json") as fin:
        data = json.load(fin)
    for component, vals in data["repositories"].items():
        for k, v in [('branchname', 'id'), ('repository', 'repository')]:
            name = conv(component + '_' + k)
            value = vals[v]
            print("{0} {1}".format(name, value), file=out)
    print("RELEASE {0}".format(data["release"]), file=out)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        output = open(sys.argv[1], "w")
    else:
        output = sys.stdout
    main(output)
