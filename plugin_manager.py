# gitter, An IRC-bot for broadcasting changes to git repositories
# Copyright (c) 2014 firecoders
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import importlib
import traceback
import re

import sys
if sys.version_info.minor < 4:
    from imp import reload as reload_module
else:
    from importlib import reload as reload_module

plugins = {}
dependencies = {}
reverse_dependencies = {}
registered_plugins = []

def register ():
    name = extract_calling_plugin_name ()
    if name not in dependencies:
        dependencies [ name ] = []
    if name not in reverse_dependencies:
        reverse_dependencies [ name ] = []
    if name not in registered_plugins:
        registered_plugins.append ( name )

def get ( name ):
    if name in plugins:
        return plugins [ name ]

    requester = extract_calling_plugin_name ()
    if requester and requester not in registered_plugins:
        raise Exception ( "Plugin %s didn't register!" % requester )

    print ( "Loading plugin %s..." % name )
    plugin = importlib.import_module ( "plugins.%s" % name )
    if name not in registered_plugins:
        reload_module ( plugin )
    plugins [ name ] = plugin

    if name not in registered_plugins:
        raise Exception ( "Plugin %s didn't register!" % name )

    if requester:
        add_dependency ( requester, name )

    return plugins [ name ]

def unload ( name, cleanup = True ):
    if name not in plugins:
        return
    print ( "Unloading plugin %s..." % name )
    try:
        plugins [ name ].unload ()
    except AttributeError:
        print ( "Plugin %s does not implement the unload function!" % name )
    if cleanup:
        for plugin in dependencies [ name ]:
            reverse_dependencies [ plugin ].remove ( name )
            if cleanup and can_unload ( plugin ):
                unload ( plugin )
        del dependencies [ name ]
    del plugins [ name ]
    registered_plugins.remove ( name )

def reload ( name, cleanup = False, recursive = True ):
    plugins = []
    def add_plugin ( name ):
        for plugin in reverse_dependencies [ name ]:
            add_plugin ( plugin )
        plugins.append ( name )
    if recursive:
        add_plugin ( name )
    else:
        plugins.append ( name )
    plugins.reverse ()
    for plugin in plugins:
        unload ( plugin, cleanup = cleanup )
    for plugin in plugins:
        get ( plugin )

def can_unload ( name ):
    return len ( reverse_dependencies [ name ] ) == 0

def add_dependency ( plugin_name, needed_name ):
    if needed_name not in dependencies [ plugin_name ]:
        dependencies [ plugin_name ].append ( needed_name )
    if plugin_name not in reverse_dependencies [ needed_name ]:
        reverse_dependencies [ needed_name ].append ( plugin_name )

def extract_calling_plugin_name ():
    stack = traceback.extract_stack ()
    filename = stack [ - 3 ] [ 0 ]
    match = re.match ( r".*/plugins/(.*?)\.py", filename )
    if match:
        return match.group ( 1 ).replace ( '/', '.' )
