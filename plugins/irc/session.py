import plugin_manager

plugin_manager.register ()

utils = plugin_manager.get ( 'utils' )

irc = utils.Container ()
irc.server = plugin_manager.get ( 'irc.server' )
irc.channel = plugin_manager.get ( 'irc.channel' )
irc.config = plugin_manager.get ( 'irc.config' )

serv = irc.server.Server ( irc.config.domain, irc.config )
chan = irc.channel.Channel ( serv, irc.config.channel )

def unload ():
    chan.part ()
    serv.disconnect ()
