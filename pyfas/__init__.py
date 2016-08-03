import os
from pyfas.tpl import Tpl
from pyfas.ppl import Ppl
from pyfas.genkey import Genkey
from pyfas.tab import Tab
if os.name == "nt":
    from pyfas.pilink import PI_read
