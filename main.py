#!/usr/bin/env python3

import time
import plugin_manager

if __name__ == '__main__':
    main = plugin_manager.get ( 'main' )
    while main.active:
        time.sleep ( 2 )
        if main.reload_plugin:
            plugin_manager.reload ( main.reload_plugin )
            main.reload_plugin = None
    plugin_manager.unload ( 'main' )
