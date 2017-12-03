#!/bin/bash
# Utility script for running crawlers

usage="
  Usage: `basename $0` [-h] [-t n]

  where:
    -h    show help text
    -t    set how long to run spiders for (in seconds)
"

while getopts ':ht:' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
    t) time=$OPTARG
       ;;
    :) printf "  Missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "  Illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done

echo 'Spinning up crawlers...'
cd sleuth_crawler/scraper
python crawl.py & read -t $time ; kill $!
echo 'Crawler run for ' $time ' seconds'