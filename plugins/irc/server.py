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

import socket
import time
import threading

import push_analyzer.utils.observer
from push_analyzer.utils.misc import utc_timestamp

import plugin_manager

plugin_manager.register ()

utils = plugin_manager.get ( 'utils' )
irc = utils.Container ()
irc.parser = plugin_manager.get ( 'irc.parser' )

class Server:
    def __init__ ( self, domain, conf ):
        self.conf = conf
        self.domain = domain
        self.readbuffer = ''
        self.active = True
        self.message_timer = utc_timestamp ()

        self.messages = push_analyzer.utils.observer.Signal ()
        self.connected = push_analyzer.utils.observer.Signal ()
        self.socket = socket.socket ()
        self.connect ()
        self.loop_thread = threading.Thread ( target = self.loop )
        self.loop_thread.start ()

    def __del__ ( self ):
        self.disconnect ()

    def loop ( self ):
        while self.active:
            lines = self.read_lines ()
            for line in lines:
                if line.startswith ( 'PING' ):
                    self.send_message ( line.replace ( 'PING', 'PONG' ) )
                parsed = irc.parser.parse_message ( line )
                if parsed.type == 'PRIVMSG':
                    self.messages ( parsed )

    def connect ( self ):
        reconnect_wait = 15
        socket_open = False
        while not socket_open:
            self.socket.close ()
            self.socket = socket.socket ()
            try:
                self.socket.connect ( ( self.domain, 6667 ) )
                socket_open = True
            except socket.gaierror:
                print ( "Connecting failed, will retry in %d seconds..." % reconnect_wait )
                time.sleep ( reconnect_wait )
                reconnect_wait *= 2
                if reconnect_wait > 300:
                    reconnect_wait = 300

        self.send_message ( "NICK %s" % self.conf.nick )
        self.send_message ( "USER bot localhost localhost :%s" % self.conf.description )

        accepted = False
        while not accepted:
            for line in self.read_lines ( timeout = None ):
                if ':Nickname is already in use' in line:
                    print ( 'Name already taken. Trying again in 2 minutes.' )
                    time.sleep ( 120 )
                    self.connect ()
                    break

                elif ":%s MODE %s :" % ( self.conf.nick, self.conf.nick ) in line:
                    print ( "Connection accepted!" )
                    accepted = True
                    break
        self.connected ()

    def disconnect ( self ):
        self.active = False
        self.loop_thread.join ( timeout = 5 )
        self.send_message ( "QUIT :%s" % self.conf.quit_message )

    def send_message ( self, message ):
        now = utc_timestamp ()
        if self.message_timer < now:
            self.message_timer = now
        if self.message_timer < now + 10:
            print ( "-> %s" % message )
            self.socket.send ( message.encode () + b"\r\n" )
            self.message_timer += 2
        else:
            print ( "Sleeping for %d seconds to prevent flooding %s" % ( self.conf.flood_sleeptime, self.domain ) )
            time.sleep ( self.conf.flood_sleeptime )
            self.send_message ( message )

    def read_lines ( self, timeout = 200 ):
        self.socket.settimeout ( timeout )
        try:
            self.readbuffer = self.readbuffer + self.socket.recv ( 1024 ).decode ()
            readlines = self.readbuffer.split ( "\r\n" )
            # the last item in the list is a cut-off message
            self.readbuffer = readlines.pop ()
            for line in readlines:
                try:
                    print ( "<- %s" % line )
                except UnicodeEncodeError:
                    print ( "Oh noes, %s sent some magic characters we can't encode!" % self.domain )
            return readlines
        except socket.timeout:
            print ( "Connection to %s lost. will reconnect in 10 seconds." % self.domain )
            time.sleep ( 10 )
            self.connect ()
            return self.read_lines ( timeout = timeout )
