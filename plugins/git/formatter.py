import push_analyzer.utils.observer
import push_analyzer.utils.git as git

import plugin_manager

plugin_manager.register ()

output = push_analyzer.utils.observer.Signal ()

templates = {
    'create branch' : 'Branch `{name}` added.',
    'remove branch' : 'Branch `{name}` removed.',
    'update'        : 'Commits were added to `{name}`:',
    'forced update' : 'The history of `{name}` was changed:',
    'add'           : 'Commit `{shortsha}` [{message}] added.',
    'remove'        : 'Commit `{shortsha}` [{message}] removed.',
    'move'          : 'Commit `{shortto}` [{msgto}] that was added is the previous `{shortfrom}`',
}

def format ( url, changes ):
    output ( url )
    for change in changes:
        msg = templates [ change [ 'type' ] ]
        if 'sha' in change:
            change [ 'shortsha' ] = change [ 'sha' ] [ : 7 ]
            change [ 'message' ] = git.get_message ( change [ 'sha' ] )
        if 'from' in change:
            change [ 'shortfrom' ] = change [ 'from' ] [ : 7 ]
            change [ 'msgfrom' ] = git.get_message ( change [ 'from' ] )
        if 'to' in change:
            change [ 'shortto' ] = change [ 'to' ] [ : 7 ]
            change [ 'msgto' ] = git.get_message ( change [ 'to' ] )
        output ( msg.format ( **change ) )
    output ( '---' )
