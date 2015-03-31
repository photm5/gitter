import push_analyzer.utils.observer

import plugin_manager

plugin_manager.register ()

class Channel:
    def __init__ ( self, server, name ):
        self.server = server
        self.name = name

        self.messages = push_analyzer.utils.observer.Signal ()
        self.server.messages.subscribe ( self.handle_message )

        self.server.connected.subscribe ( self.join )
        self.join ()

    def __del__ ( self ):
        self.part ()

    def join ( self ):
        print ( "Joining channel %s..." % self.name )
        self.server.send_message ( "JOIN %s" % self.name )

    def part ( self ):
        print ( "Leaving channel %s..." % self.name )
        self.server.send_message ( "PART %s" % self.name )

    def write ( self, message ):
        self.server.send_message ( "PRIVMSG %s :%s" % ( self.name, message ) )

    def handle_message ( self, parsed ):
        if parsed.channel == self.name:
            self.messages ( parsed )
