# -*- coding: utf-8 -*-

# Scrapy settings for courses_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

import sys
import os.path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path = sys.path + [os.path.join(PROJECT_ROOT, '../../..'), os.path.join(PROJECT_ROOT, '../..')]

BOT_NAME = 'sleuth_scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# List approved starting URLs to be crawled by BroadCrawler
# Place specific domains before www.ubc.ca
PARENT_URLS = [
    'https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=0',
    'https://www.ubyssey.ca',
    'https://www.ubc.ca',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'courses_scraper (+http://www.yourdomain.com)'

### Custom Settings:

# Process lower depth requests first
DEPTH_PRIORITY = 50

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Enable SSL Handshakes
DOWNLOADER_CLIENTCONTEXTFACTORY = 'scraper.customcontext.CustomContextFactory'

# Built-in Logging Level (alternatively use DEBUG outside production)
LOG_LEVEL = 'INFO'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# Increase max thread pool size for DNS queries
REACTOR_THREADPOOL_MAXSIZE = 20

# Disable retrying failed HTTP requests (ie for slow websites)
#RETRY_ENABLED = False

# Reduce download timeout to discard stuck requests quickly
DOWNLOAD_TIMEOUT = 15

# EXPERIMENTAL: We shouldn't have to follow redirects
#REDIRECT_ENABLED = False

# EXPERIMENTAL: Ajax Crawlable Pages are rare but apparently can help
# crawl certain web pages faster. Could have both positive and negative
# performance ramifications
# https://doc.scrapy.org/en/latest/topics/broad-crawls.html#enable-crawling-of-ajax-crawlable-pages
AJAXCRAWL_ENABLED = True

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'scraper.pipelines.SolrPipeline': 300,
# }

### Scrapy Defaults and Other Options:

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'courses_scraper.middlewares.CoursesScraperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'courses_scraper.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
