#!/usr/bin/env bash

set -e


DBDUMP_DIR="$1"
ODOO_DIR="$2"
export DBDUMP_DIR ODOO_DIR

if [[ "$3" ]] ; then
    ENTERPRISE_DIR="$3"
    export ENTERPRISE_DIR
fi

exec python -m unittest discover tests
