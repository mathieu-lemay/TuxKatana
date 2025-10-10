from gi.repository import GObject

from .tsl import TSLFile

import logging
from lib.log_setup import LOGGER_NAME
log = logging.getLogger(LOGGER_NAME)

class Presets(GObject.GObject):
    num = GObject.Property(type=int, default=-1)
    name = GObject.Property(type=str)
    # label = GObject.Property(type=str)
    # channel = GObject.Property(type=int)

#class Preset(TSLFile, GObject.GObject):
#    def __init__(self, ctrl):
#        super().__init__(ctrl)
#        self.ctrl = ctrl

#    def set_list_presets(self):
#        log.debug("--")
 
#        #self.tsl = TSLFile(device)

#    def gen(self):
#        self.save()
