#!/usr/local/bin/python

import operator
from includes import *

def top_ip(limit):
	if limit == None:
		limit = shared.default_top

	print
	print 'Find %r top ips...' % limit
	data = load_data()
	ips = {}
	for stats in data:
		if not stats.ip in ips:
			ips[stats.ip] = 0
		ips[stats.ip] += 1

	display_stats(ips, limit)

def top_url(limit):
	if limit == None:
		limit = shared.default_top

	print
	print 'Find %r top urls...' % limit
	data = load_data()
	urls = {}
	for stats in data:
		if not stats.url in urls:
			urls[stats.url] = 0
		urls[stats.url] += 1

	display_stats(urls, limit, outformat='{1} times : {0}')


def top_user_agent(limit):
	if limit == None:
		limit = shared.default_top

	print
	print 'Find %r top user agents...' % limit
	data = load_data()
	uas = {}
	for stats in data:
		if not stats.useragent in uas:
			uas[stats.useragent] = 0
		uas[stats.useragent] += 1

	display_stats(uas, limit, outformat='{1} times : {0}')