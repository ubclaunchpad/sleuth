#!/bin/bash
# Runs all crawlers

echo 'Spinning up crawlers...'
cd sleuth_crawler/scraper
python crawl.py & read -t 10 ; kill $!
