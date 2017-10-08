#!/bin/bash
# Wait until services have booted, then run the given command

set -e

condition=$1
shift
cmd="$@"

>&2 echo "Waiting for service"
until exec $condition; do
  sleep 10
done
>&2 echo "Service ready"

exec $cmd