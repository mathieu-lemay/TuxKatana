import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject

import logging
from lib.log_setup import LOGGER_NAME
log = logging.getLogger(LOGGER_NAME)

from widgets.toggle import Toggle

class Bank(Gtk.Grid):
    selected = GObject.Property(type=int, default=-1)
    single_list = GObject.Property(type=object)

    def __init__(self, label, buttons, single=False, color_sw=False, ctrl=None):
        super().__init__(column_spacing=1, row_spacing=1)
        self.set_column_homogeneous(True)
        self.get_style_context().add_class("inner")
        self.ctrl = ctrl
        self.name = label
        self.single = single
        self.labels = []
        if label in ['BANK_A', 'BANK_B']:
            self.ctrl.connect("set-preset-name", self.on_set_preset_name)
            for i, name in enumerate(buttons):
                self._add_label(i, name)
        elif label == 'EFFECTS':
            self.ctrl.connect("set-effect-name", self.on_set_effect_name)
            for i, name in enumerate(buttons):
                idx = i
                if name != "DELAY_R":
                    # if name == "REVERB":
                        # idx -= 1
                    self._add_label(idx, name)

        self.buttons = []
        for i, name in enumerate(buttons):
            if name != 'DELAY_R':
                but = Toggle( name, buttons[name] )
                but.handler_id = but.connect("toggled", self.on_toggled,i)
                but.set_hexpand(True)
                but.set_halign(Gtk.Align.FILL)
                self.buttons.append(but)
                self.attach(but, i, 1, 1, 1)
        if not self.single:
            self.connect("notify::selected", self.on_selected)

    def on_set_effect_name(self, widget, idx, name):
        if self.labels[idx].get_label() != name:
            self.labels[idx].set_label(name)
            log.debug(f"{idx=} {name=}")

    def on_set_preset_name(self, widget, idx, name):
        # log.debug(f"{self.labels} {self.name}: {name} ({idx})")
        if self.name == 'BANK_A' and idx<4:
            self.labels[idx].set_label(name)
        elif self.name == 'BANK_B':
            self.labels[idx-4].set_label(name)

    def _add_label(self, idx, name):
        log.debug(f"{idx=} {name=}")
        lbl = Gtk.Label(label=name)
        lbl.get_style_context().add_class('no-margin')
        lbl.set_hexpand(False)
        self.labels.append(lbl)
        self.attach( lbl, idx, 0, 1, 1)


    def on_selected(self, obj, pspec):
        #log.debug(f"bank.on_selected({self.selected})")
        button = self.buttons[obj.selected]
        button.handler_block(button.handler_id)
        button.set_active(True)
        self.set_inactives(button)
        button.handler_unblock(button.handler_id)

           
    def on_toggled(self, widget, idx):
        # log.debug(f"{widget.name}: {widget.get_active()}" )
        if not self.single or hasattr(self, "f_bank"):
            self.set_property("selected", idx)
            self.set_inactives( widget )
            if hasattr(self, "f_bank"):
                self.f_bank.set_inactives()

    def set_inactives( self, widget=None ):
        for button in self.buttons:
            if button != widget and button.get_active():
                button.handler_block(button.handler_id)
                button.set_active(False)
                button.handler_unblock(button.handler_id)


