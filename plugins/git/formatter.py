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
    'add'           : 'Add    [{shortsha}] {message}',
    'remove'        : 'Remove [{shortsha}] {message}',
    'move'          : 'Reuse  [{shortfrom}] as [{shortto}] {msgto}',
}

def format_changeset ( url, changes ):
    overview = changes [ 0 ]
    if overview [ 'type' ] == 'update':
        output ( templates [ 'update' ].format ( **overview ) )
        for change in changes [ 1 : ]:
            output ( "[%s] %s" % ( change [ 'sha' ] [ : 7 ], git.get_message ( change [ 'sha' ] ) ) )
    else:
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

def format ( url, changes ):
    output ( url )
    while changes:
        changeset = []
        changeset.append ( changes [ 0 ] )
        changes.pop ( 0 )
        for change in changes [ : ]:
            if change [ 'type' ] in [ 'update', 'forced update', 'create branch', 'remove branch' ]:
                break
            changeset.append ( change )
            changes.remove ( change )
        format_changeset ( url, changeset )
    output ( '---' )
