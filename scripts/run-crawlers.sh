#!/bin/bash
# Utility script for running crawlers

re='^[0-9]+$'
if ! [[ $1 =~ $re ]] ; then
  echo "Must specify number of seconds to run crawlers for" >&2
  exit 1
fi

cd sleuth_crawler/scraper
echo "Spinning up crawlers..."
python crawl.py & read -t $1
kill $!
echo "Crawlers ran for $1 seconds"