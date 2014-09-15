#!/usr/bin/env python3

import time
import plugin_manager

if __name__ == '__main__':
    try:
        main = plugin_manager.get ( 'main' )
        while main.active:
            time.sleep ( 2 )
            if main.reload_plugin:
                plugin_manager.reload ( main.reload_plugin )
                main.reload_plugin = None
        plugin_manager.unload ( 'main' )
    except Exception as e:
        print ( '===' )
        print ( 'Exception catched in main.py:' )
        print ( e )
        print ( 'Unloading plugins...' )
        print ( '===' )
        while len ( plugin_manager.plugins ) > 0:
            plugin_manager.unload ( list ( plugin_manager.plugins.keys () ) [ 0 ] )
        raise e
