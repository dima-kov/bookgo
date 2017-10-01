from importlib import import_module

from .common import *

try:
    from .prod import *
except ImportError:
    try:
        from .local import *
    except ImportError:
        try:
            from .front import *
        except ImportError:
            pass

'''
# globals().update(import_module('bocrok.settings.common').__dict__)
# settings = ['prod', 'local', 'front']

# for settings_file in settings:
#     try:
#         import_filename = 'bocrok.settings.{}'.format(settings_file)
#         globals().update(import_module(import_filename).__dict__)
#         break
#     except ImportError:
#         pass
'''
