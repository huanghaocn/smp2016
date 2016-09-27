# -*- coding: utf-8 -*-

# Scrapy settings for weibo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weibo'

SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'weibo (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8
# PROXIES = [
#     {'ip_port': '58.56.21.196:80', 'user_pass': None},
#     # {'ip_port': '115.28.101.222:3128', 'user_pass': None},
#     {'ip_port': '58.214.254.46:8080', 'user_pass': None},
#     {'ip_port': '58.56.21.201:80', 'user_pass': None},
#     {'ip_port': '180.212.126.197:8080', 'user_pass': None},
#     {'ip_port': '58.56.21.198:80', 'user_pass': None},
#     {'ip_port': '60.191.159.86:3128', 'user_pass': None},
#     {'ip_port': '123.125.122.224:80', 'user_pass': None},
#     {'ip_port': '60.21.209.114:8080', 'user_pass': None}
# ]
# PROXIES = [
#     {'ip_port': '120.25.235.11:8089', 'user_pass': None},
#     {'ip_port': '120.192.92.98:80', 'user_pass': None},
#     {'ip_port': '111.13.136.46:80', 'user_pass': None},
#     {'ip_port': '111.11.122.7:80', 'user_pass': None},
#     {'ip_port': '183.245.146.237:80', 'user_pass': None},
#     {'ip_port': '111.12.251.174:80', 'user_pass': None},
#     {'ip_port': '112.16.21.18:2226', 'user_pass': None},
#     {'ip_port': '111.12.251.169:80', 'user_pass': None},
#     {'ip_port': '111.12.251.167:80', 'user_pass': None}
# ]
# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN=16
CONCURRENT_REQUESTS_PER_IP=1
DOWNLOAD_TIMEOUT =2
# Disable cookies (enabled by default)
# COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED=False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'weibo.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'weibo.middlewares.ProxyMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'weibo.pipelines.SomePipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
# AUTOTHROTTLE_ENABLED=True
# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED=True
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
