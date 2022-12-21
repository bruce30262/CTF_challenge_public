#!/usr/bin/env sh
find ./www -type d -not -path "*mojo_bindings*" -not -path "./www" | xargs rm -rf
