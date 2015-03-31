from push_analyzer.utils.misc import home_directory

import plugin_manager

plugin_manager.register ()

poll_interval = 20
work_dir = home_directory + '/gitter/'
urls = [
    'https://github.com/shak-mar/gitter.git',
]
