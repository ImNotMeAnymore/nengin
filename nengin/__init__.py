import os
if os.environ.get("NENGIN_BACKEND") == "opengl": from .glnengin import *
else: from .nengin import *