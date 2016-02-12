#!/usr/bin/python

#
#   Config file ddos-log-analysis.conf should contain:
#
#[MAIN]
#log_match = [filename regex] 
#time_range = <BEGIN:Y-M-D_h:m>,<END:Y-M-D_h:m> or <BEGIN:Y-M-D_h:m>
#output_file = /var/log/ddos-log-analysis.log

import subprocess, time, re, ConfigParser, logging, sys, os, argparse, fcntl, logging, glob
from datetime import datetime
from stats import *
from includes import *

pid_file = '/var/run/ddos-log-analysis.pid'
logfile = ""
configfile = "/etc/ddos-log-analysis.conf"


class StreamToLogger(object):
   """
   Fake file-like stream object that redirects writes to a logger instance.
   """
   def __init__(self, logger, log_level=logging.INFO):
      self.logger = logger
      self.log_level = log_level
      self.linebuf = ''
 
   def write(self, buf):
      for line in buf.rstrip().splitlines():
         self.logger.log(self.log_level, line.rstrip())	
		
# be sure runs only once
fp = open(pid_file, 'w')
try:
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    # another instance is running
    sys.exit(0)

class AppendArgConst(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest,
                 nargs=None,
                 const=None,
                 default=None,
                 type=None,
                 choices=None,
                 required=False,
                 help=None,
                 metavar=None):
        argparse.Action.__init__(self,
                                 option_strings=option_strings,
                                 dest=dest,
                                 nargs=nargs,
                                 const=default,
                                 default=[],
                                 type=type,
                                 choices=choices,
                                 required=required,
                                 help=help,
                                 metavar=metavar,
                                 )

        self.function = const
        return

    def __call__(self, parser, namespace, values, option_string=None):
        #print 'Processing AppendArgConst for "%s"' % self.dest
        #print '  parser = %s' % id(parser)
        #print '  values = %r' % values
        #print '  option_string = %r' % option_string        
        #print '  self = %r' % self        

        # Do some arbitrary processing of the input values
        if not isinstance(values, list):
            values = ["{0}|{1}".format(values, self.function)]

        #print '  values = %r' % values
        # Save the results in the namespace using the destination
        # variable given to our constructor.
        existing = getattr(namespace, self.dest)
        existing += values
        setattr(namespace, self.dest, existing)

parser = argparse.ArgumentParser(description='Analyse apache logs after ddos.')
parser.add_argument('-l', '--log', type=str, metavar='path', nargs='?', dest='analysis_path', help='<regex log filename> or --log <regex logfilename>')
parser.add_argument('-p', '--progress', dest='progress', action='store_true', help='<regex log filename> or --log <regex logfilename>')
parser.add_argument('-t', '--time-range', metavar='<Y-M-D h:m> (Y-M-D h:m>)', default=[0, -1], type=str, nargs='*', dest='timerange', help='<BEGIN:Y-M-D h:m> <END:Y-M-D h:m> or <BEGIN:Y-M-D h:m>>')
parser.add_argument('-o', '--out', type=argparse.FileType('w'), metavar='FILE', nargs='?', dest='logfile', help='<path>')
parser.add_argument('--config-file', type=argparse.FileType('r'), metavar='FILE', nargs='?', dest='configfile', help='<path>')
parser.add_argument('--top-ip', metavar='N', nargs='?', default=shared.default_top, dest='actions', action=AppendArgConst, const='top_ip', help='<option: number (default=20)> ')
parser.add_argument('--top-url', metavar='N', nargs='?', default=shared.default_top, dest='actions', action=AppendArgConst, const='top_url', help='<option: number (default=20)> ')
parser.add_argument('--top-user-agent', metavar='N', nargs='?', default=shared.default_top, dest='actions', action=AppendArgConst, const='top_user_agent', help='<option: number (default=20)> ')
parser.add_argument('--top-live-ip', metavar='N', nargs='?', default=shared.default_top, dest='actions', action=AppendArgConst, const='top_live_ip', help='<option: number (default=20)> ')


args = parser.parse_args()
if args.actions is None:
	actions = []

if args.timerange is not None:
	#trange = shared.timerange.split(',')
	shared.time_range_begin = datetime.strptime(args.timerange[0], shared.arg_date_format)
	if len(args.timerange) > 1:
		shared.time_range_end = datetime.strptime(args.timerange[1], shared.arg_date_format)

if args.analysis_path is not None:
	shared.analysis_path = args.analysis_path

if args.progress is not None:
	shared.progress = args.progress

for action in args.actions:
	arg, fun = action.split('|', 1)
	globals()[fun]( int(arg) )
	#fun(arg)
