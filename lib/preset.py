from gi.repository import GObject
import os

from .tsl import TSLParser

import logging
from lib.log_setup import LOGGER_NAME
log = logging.getLogger(LOGGER_NAME)

class Preset(GObject.GObject, TSLParser):
    chan = GObject.Property(type=int, default=-1)
    name = GObject.Property(type=str)
    def __init__(self, chan=-1, name=None):
        super().__init__(name=name, chan=chan)
        log.debug(f"{chan=} {name=}")
        # else:
        #     TSLParser.__init__(self, self)
        # if ui:
        #     self.ui = ui
        #     self.load("James_Ryan_multi_read.tsl")


 
#class Preset(TSLFile, GObject.GObject):
#    def __init__(self, ctrl):
#        super().__init__(ctrl)
#        self.ctrl = ctrl

#    def set_list_presets(self):
#        log.debug("--")
 
#        #self.tsl = TSLFile(device)

#    def gen(self):
#        self.save()
