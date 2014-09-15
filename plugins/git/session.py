import pathlib
import functools
import threading

import push_analyzer.utils.git as git
import push_analyzer.utils.system as system
import push_analyzer.poller
import push_analyzer.analyzer
import push_analyzer.utils.observer

import plugin_manager

plugin_manager.register ()
config = plugin_manager.get ( 'git.config' )

output = push_analyzer.utils.observer.Signal ()

pollers = {}

def analyze ( url, stamp_pre, stamp_post ):
    refs_pre = pollers [ url ].revisions [ stamp_pre ]
    refs_post = pollers [ url ].revisions [ stamp_post ]
    repo_name = git.extract_repo_name ( url )
    with system.cd ( config.work_dir + repo_name ):
        results = push_analyzer.analyzer.analyze_push ( refs_pre, refs_post )
        output ( url, results )

for url in config.urls:
    pollers [ url ] = push_analyzer.poller.Poller ( url, work_dir = config.work_dir, interval = config.poll_interval )
    pollers [ url ].ref_change.subscribe ( functools.partial ( analyze, url ) )
    threading.Thread ( target = pollers [ url ].loop ).start ()

def unload ():
    for url in config.urls:
        pollers [ url ].stop ()
