#!/bin/bash
# Wait until services have booted, then run the given command
# The first argument should be the name of the service, the second should
# be the command to wait on. Once that command is run, the rest of the arguments
# will be run as a command.

set -e

name=$1
condition=$2
shift
cmd="$@"

>&2 echo "Waiting for $1"

while true; do
  if eval "$condition"; then
    break
  fi
  sleep 10
done

>&2 echo "$1 ready"
eval $cmd