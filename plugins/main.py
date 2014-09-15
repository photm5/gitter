import time

import plugin_manager

plugin_manager.register ()

irc_session = plugin_manager.get ( 'irc.session' )

pollers = plugin_manager.get ( 'git.session' )
formatter = plugin_manager.get ( 'git.formatter' )
pollers.output.subscribe ( formatter.format )
formatter.output.subscribe ( irc_session.chan.write )

def handle_message ( parsed ):
    global active, reload_plugin
    if parsed.content.startswith ( 'gitter, reload ' ):
        plugin = parsed.content.replace ( 'gitter, reload ', '' )
        if plugin not in plugin_manager.registered_plugins:
            irc_session.chan.write ( "No `%s` plugin is currently registered." % plugin )
        else:
            reload_plugin = plugin
    elif parsed.content == "gitter, quit please":
        active = False

irc_session.chan.messages.subscribe ( handle_message )

active = True
reload_plugin = None

def unload ():
    irc_session.chan.messages.unsubscribe ( handle_message )
    pollers.output.unsubscribe ( formatter.format )
    formatter.output.unsubscribe ( irc_session.chan.write )
