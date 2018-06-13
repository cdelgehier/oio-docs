#!/usr/bin/env bash
set -e
set -x

TARGET=$(readlink --canonicalize result-docs)
BUILD=$(readlink --canonicalize "$1")
[[ -n "$BUILD" ]]

mkdir -p $TARGET

if [[ -z "$OIO_DOCS_LIGHT" ]]; then

    # Prepare an environment for the building process
    mkdir -p "$BUILD"
    ./bin/gen-vars.py "$BUILD/vars.export"

    # Generate the RAWX API
    ./bin/extract-doc.py --tag=RAWX \
      $(find $BUILD/oio-sds/rawx-apache2/src -type f -name '*.c' -or -name '*.h') \
      > doc/source/sdk-guide/rawx_api_calls.rst

    ./bin/extract-doc.py --tag=CS \
      $(find $BUILD/oio-sds/proxy -type f -name '*.c' -or -name '*.h') \
      > doc/source/sdk-guide/proxy_cs_api_calls.rst

    ./bin/extract-doc.py --tag=DIR \
      $(find $BUILD/oio-sds/proxy -type f -name '*.c' -or -name '*.h') \
      > doc/source/sdk-guide/proxy_dir_api_calls.rst

    ./bin/extract-doc.py --tag=CONTAINER \
      $(find $BUILD/oio-sds/proxy -type f -name '*.c' -or -name '*.h') \
      > doc/source/sdk-guide/proxy_container_api_calls.rst

    ./bin/extract-doc.py --tag=RDIR \
      $(find $BUILD/oio-sds/rdir -type f -name '*.c' -or -name '*.h') \
      > doc/source/sdk-guide/rdir_api_calls.rst

    ./bin/extract-doc.py --tag=ACCT \
      $(find $BUILD/oio-sds/oio/account -type f -name '*.py') \
      > doc/source/sdk-guide/acct_api_calls.rst

    # # Build the oio-sds variables
    $BUILD/oio-sds/confgen.py rst "$BUILD/oio-sds/conf.json" \
      doc/source/admin-guide/variables.rst || true

    # Build the Java API javadoc
    if which javadoc 2>/dev/null >/dev/null ; then
      if [[ -d $BUILD/oio-api-java/src/main/java ]] ; then
        ( cd $BUILD/oio-api-java/src/main/java \
          && javadoc -d $TARGET/oio-api-java-doc io.openio.sds )
      fi
    fi


    # Build the C API doxygen doc
    if which doxygen 2>/dev/null >/dev/null ; then
      if [[ -r doc/Doxyfile-api-c ]] ; then
        doxygen doc/Doxyfile-api-c
      fi
    fi

    # We configured sphinx to make it document the python sdk. The modules will
    # be loaded, we need even the dependencies.
    cd "$BUILD/oio-sds" \
      && pip install --upgrade -r test-requirements.txt \
      && pip install --upgrade -r all-requirements.txt \
      && python ./setup.py install

    # Build the Python API sphinx doc
    if [[ -d "$BUILD/oio-sds/oio" ]] ; then
    sphinx-apidoc --ext-autodoc -o doc2/source/sdk-guide/python-api "$BUILD/oio-sds/oio"
    fi
fi

# Generate a copy of all the sources to patch them, in order to expose
# the release of each component
if [[ -d doc2 ]] ; then
  rm -rf doc2
fi
cp -rp doc doc2

SED='sed -i '
while read K V ; do
  SED="${SED}-e s,{{$K}},$V,g "
done < "${BUILD}/vars.export"

find doc2/ -type f -name '*.rst' | while read P ; do
  $SED "$P"
done

# Patch conf.py with components.json
if cat components.json | python -mjson.tool | grep stable | grep true; then
    sed -i 's/\(.*stable.*\)\(False\)\(.*\)/\1True\3/g' doc2/conf.py
fi

sphinx-build -v -E -d /tmp/sphinx doc2 $TARGET


# Patch all HTML to remove generated CSS theme
set +x
for file in $(find $TARGET -name "*.html")
do
    sed -i '/basic\.css/d' $file
done
set -x
