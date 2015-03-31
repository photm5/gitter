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
