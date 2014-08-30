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

import plugin_manager

plugin_manager.register ()
utils = plugin_manager.get ( 'utils' )

def parse_message ( message ):
    parsed = utils.Container ()
    split = message.split ( ' ' )
    parsed.origin = split [ 0 ]
    if '!' in parsed.origin:
        parsed.name = split [ 0 ] [ 1 : split [ 0 ].find ( '!' ) ]
    parsed.type = split [ 1 ]
    if len ( split ) > 2:
        parsed.channel = split [ 2 ]
    if len ( split ) > 3:
        split [ 3 ] = split [ 3 ] [ 1 : ]
        parsed.content = ' '.join ( split [ 3 : ] )
    return parsed
