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
