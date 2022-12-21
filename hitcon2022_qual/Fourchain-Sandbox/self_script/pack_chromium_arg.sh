#!/bin/bash

set -Eeuo pipefail

# print all commands that are executed
set -x

DIR=$1

if [ ! -d ${DIR} ]; then
    echo "${DIR} not exist"
    exit 1
fi

if [ -d chromium ]; then
  rm -R chromium
fi
mkdir -p chromium

if [ -d mojo_bindings ]; then
  rm -R mojo_bindings
fi
mkdir -p mojo_bindings

for f in chrome chrome_100_percent.pak chrome_200_percent.pak icudtl.dat product_logo_48.png resources.pak snapshot_blob.bin v8_context_snapshot.bin; do
  cp $DIR/$f chromium/
done

strip chromium/chrome

cp $DIR/gen/mojo/public/js/mojo_bindings.js mojo_bindings/

pushd $DIR/gen
for f in $(find -name '*.mojom.js'); do
  TMP_DIR=$HOME/test/hitcon2022/mojo_bindings/$(dirname "$f")
  mkdir -p "${TMP_DIR}" 2>/dev/null || true
  cp "$f" "${TMP_DIR}/"
done
popd

rm chromium.tar.xz || true
tar -I "pixz -9 -p 20" -cf chromium.tar.xz chromium/

rm mojo_bindings.tar.xz || true
tar -I "pixz -9 -p 20" -cf mojo_bindings.tar.xz mojo_bindings/

echo "Done! Don't forget to update the exploit."
