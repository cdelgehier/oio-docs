#!/usr/bin/env python

import json
import sys
import os.path
import subprocess


def exec_commands(commands, exit=True):
    commands.insert(0, "set -x")
    commands.insert(0, "set -e")
    status = subprocess.call("\n".join(commands), shell=True)
    if exit and status != 0:
        sys.exit(status)


def clone_project(destdir, repository, url, id_):
    print "\n### %s (%s)" % (repository, id_)
    repodir = '/'.join((destdir, repository))
    if not os.path.exists(repodir):
        src = os.getcwd()
        os.chdir(destdir)
        exec_commands(["git clone %s" % url])
        os.chdir(src)
    else:
        src = os.getcwd()
        os.chdir(repodir)
        exec_commands(["git fetch --tags"])
        os.chdir(src)

    src = os.getcwd()
    os.chdir(repodir)
    exec_commands(["git checkout %s" % id_], exit=False)
    os.chdir(src)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Fetch the components from git repositories")
    parser.add_argument('--public', action='store_true',
                        help="only public repos")
    parser.add_argument('--doc', action='store_true',
                        help="only documented repos")
    parser.add_argument(
        '--override', action='append',
        help=("Override branch/tag for the specified repository. "
              "Ex: --override oio-swift=1.4.0"))
    parser.add_argument('--master', '--bleeding-edge',
                        action='store_true',
                        help='Use master branch for all repositories.')
    parser.add_argument('destdir', help='Destination directory')
    args = parser.parse_args()

    with open('components.json', 'r') as fin:
        components_json = json.load(fin)

    repositories = components_json["repositories"]

    try:
        os.mkdir(args.destdir)
    except OSError:
        pass

    overrides = {x[0]: x[1] for x in (y.split('=', 2) for y in args.override)}

    for name, descr in repositories.iteritems():
        url = descr["repository"]
        if args.master:
            id_ = "master"
        else:
            id_ = overrides.get(name, descr["id"])
        if args.public and not url.startswith('http'):
            continue
        if args.doc and not descr.get('doc', True):
            # skip repos tagged as useless for doc generation
            continue
        clone_project(args.destdir, name, url, id_)


if __name__ == '__main__':
    main()
