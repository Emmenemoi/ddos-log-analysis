# ddos-log-analysis
Analyze DDOS attack ex-post

usage: ddos-log-analysis.py [-h] [-l [path]] [-p]
                            [-t [<Y-M-D h:m> Y-M-D h:m>) [<Y-M-D h:m> (Y-M-D h:m> ...]]]
                            [-o [FILE]] [--config-file [FILE]] [--top-ip [N]]
                            [--top-url [N]] [--top-user-agent [N]]
                            [--top-live-ip [N]]

Analyse apache logs after ddos.

optional arguments:
  -h, --help            show this help message and exit
  -l [path], --log [path]
                        <regex log filename>
  -p, --progress        Display progress
  -t [<Y-M-D h:m> (Y-M-D h:m>) [<Y-M-D h:m> (Y-M-D h:m>) ...]], --time-range [<Y-M-D h:m> (Y-M-D h:m>) [<Y-M-D h:m> (Y-M-D h:m>) ...]]
                        <begin date> <end date> or <begin date>
  -o [FILE], --out [FILE]
                        output to FILE file
  --config-file [FILE]  load FILE as config file
  --top-ip [N]          <N: top limit (default=20)>
  --top-url [N]         <N: top limit (default=20)>
  --top-user-agent [N]  <N: top limit (default=20)>
  --top-live-ip [N]     <N: top limit (default=20)>
