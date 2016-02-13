#!/usr/local/bin/python

from __future__ import division
import subprocess, time, re, logging, sys, os, getopt, fcntl, logging, glob
from datetime import datetime, date

class SimpleProgressBar(object):
    def __init__(self, text='', maxstars=100):
        self.max = maxstars
        self.state = 0
        self.maxstars = maxstars
        self.old_display = -1
        self.text = text
        sys.stdout.write('\n')
        sys.stdout.flush()

    def _carriage_return(self):
        sys.stdout.write('\r')
        sys.stdout.flush()

    def _display(self):
		self.display = int( self.state / self.max * self.maxstars )
		if self.old_display != self.display:
			stars = ''.join(['*'] * self.display + [' '] * (self.maxstars-self.display) )
			percent = int(self.display*100/self.maxstars)
			if self.text != '':
				print '{0}: [{1}] {2}%{3}'.format(self.text, stars, percent, ''.join([' '] * self.maxstars)),
			else:
				print '[{0}] {1}%'.format(stars, percent),
			self._carriage_return()
			self.old_display = self.display

    def update(self, value=None, maximum=None):
    	if not maximum is None:
    		self.max = maximum
        if not value is None:
            self.state = value
        self._display()


class StatItem(object):
	"""docstring for StatItem"""
	def __init__(self, ip, url, useragent):
		super(StatItem, self).__init__()
		self.ip = ip
		self.url = url
		self.useragent = useragent


def load_data():
	if len(load_data.data) == 0:
		print 'Load data from {0} between {1} and {2}'.format(shared.analysis_path, shared.time_range_begin.strftime(shared.arg_date_format), shared.time_range_end.strftime(shared.arg_date_format))
		find = re.compile(shared.apacheregex, re.IGNORECASE)
		for filename in glob.glob(shared.analysis_path):
			mtime = datetime.fromtimestamp(os.path.getmtime(filename))			
			if os.path.isfile(filename) and mtime >= shared.time_range_begin :
				if shared.progress:
					spb = SimpleProgressBar(filename, 10)
					
				with open(filename) as FileObj:
					if shared.progress:
						current = 0
						spb.update(current)
						filelines = sum(1 for line in FileObj) 
						FileObj.seek(0, 0)

					for line in FileObj:
						if shared.progress:
							current += 1
							spb.update(value=current, maximum=filelines)
						try:
							parts = find.match(line)
							line_date = datetime.strptime(parts.group('datetime'), shared.apache_date_format)
						except Exception as e:
							print
							print e
							print line
						if line_date >= shared.time_range_begin and line_date <= shared.time_range_end:
							load_data.data.append( StatItem(parts.group('ip'), parts.group('url'), parts.group('agent')) )
						elif line_date > shared.time_range_end:
							if shared.progress:
								spb.update(filelines, filelines)
							break


	return load_data.data
load_data.data = []

def shared():
	shared.time_range_begin = datetime.fromtimestamp(0)
	shared.time_range_end = datetime.now()
	shared.analysis_path = "/var/log/apache2/access*.log"
	shared.apacheregex = '(?P<ip>[(\d\.)]+) - (?P<auth>.*?) \[(?P<datetime>.*?) .*?\] "(?P<url>.*?)" (?P<code>\d+) (?P<length>\d+) "(?P<referer>.*?)" "(?P<agent>.*?)"'
	shared.default_top = 20
	shared.apache_date_format = '%d/%b/%Y:%H:%M:%S'
	shared.arg_date_format = '%Y-%m-%d_%H:%M'
	shared.progress = False
shared()

def display_stats(stats, limit, outformat='{0} : {1} times'):
	print
	fullstats = sorted(stats.iteritems(), key=lambda (k,v): (v,k), reverse=True)
	count = 0
	for i,stat in enumerate(fullstats):
		if count > limit:
			return
		print outformat.format(stat[0], stat[1])
		count +=1
	print
