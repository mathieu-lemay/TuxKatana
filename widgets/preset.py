import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio #GLib, Gdk, GObject
import os

from .box_inner import BoxInner
from .file_chooser import FileChooser
from .channel_chooser import ChannelChooser

import logging
from lib.log_setup import LOGGER_NAME
log = logging.getLogger(LOGGER_NAME)

class PresetUI(Gtk.Box):
    def __init__(self, ctrl):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.ctrl = ctrl
        self.filename = None
        self.file_path = None
        self.selected_channel = None

        box_tsl = BoxInner(label="TSL File", h_box=True)
        box_tsl.set_spacing(6)

        self.append(box_tsl)

        self.reload = Gtk.Button(label="🔄")
        box_tsl.h_box.append(self.reload)
        self.reload.set_tooltip_text("Reload Preset")
        self.reload.connect("clicked", self.reload_preset)

        self.file = Gtk.Entry()
        self.file.set_hexpand(True)
        box_tsl.h_box.append(self.file)
        ext = Gtk.Label(label=".tsl   ")
        box_tsl.h_box.append(ext)

        self.save = Gtk.Button(label="💾")
        box_tsl.h_box.append(self.save)
        self.save.set_tooltip_text("Save To TSL")
        self.save.connect("clicked", self.save_tsl)

        self.open = Gtk.Button(label="📂")
        box_tsl.h_box.append(self.open)
        self.open.set_tooltip_text("Open TSL")
        self.open.connect("clicked", self.open_tsl)

        box = BoxInner(label="TSL Contained Presets", h_box=True)
        box.set_spacing(6)
        self.append(box)

        self.select = Gtk.ComboBoxText()
        self.select.set_hexpand(False)
        self.select.set_tooltip_text("Select Contained Preset")
        box.h_box.append(self.select)

        self.chan_sel = Gtk.ComboBoxText()
        self.chan_sel.set_hexpand(False)
        self.chan_sel.set_tooltip_text("Select Dest Channel")
        box.h_box.append(self.chan_sel)
        for i in range(8):
            self.chan_sel.append(str(i), f"CH_{i+1}")

        self.load = Gtk.Button(label="⬆️ ")
        box.h_box.append(self.load)
        self.load.set_halign(Gtk.Align.END)
        self.load.set_tooltip_text("Load Preset")
        self.load.connect("clicked", self.load_preset)

    def reload_preset(self, widget):
        log.debug("reload")

    def save_tsl(self, widget):
        log.debug("save")

    def load_preset(self, widget):
        log.debug("load")

    def open_tsl(self, widget):
        win = self.ctrl.parent.win
        chooser = FileChooser(win, parent=self, title="Open .tsl file")
        chooser.add_filter("TSL Files", ["*.tsl"])
        chooser.add_buttons(
            "_Cancel", Gtk.ResponseType.CANCEL,
            "_Open", Gtk.ResponseType.ACCEPT
        )
        self.file_path = chooser.choose()
        log.debug(f"{self.file_path=}")
        if self.file_path:
            self.filename = os.path.basename(self.file_path).split('.')[0]
            self.file.set_text(self.filename)

       

    def on_load_clicked(self, button):
        win = self.ctrl.parent.win
        win.set_sensitive(False)
        ch_chooser = ChannelChooser(win, self)
        ch_chooser.connect("response", self.on_channel_choosed)
        ch_chooser.show()

    def on_channel_choosed(self, dialog, response):
        win = self.ctrl.parent.win
        win.set_sensitive(True)
        if response == Gtk.ResponseType.OK:
            self.selected_channel = dialog.get_selected_channel()
            print("Choosed Channel :", self.selected_channel)
        else:
            print("Canceled")
        dialog.destroy()

    def on_save_clicked(self, button):
        #log.debug(f"{self.dest_dir+self.file_path}")
        filename = self.file.get_text()
        log.debug(filename)
        # self.own_ctrl.save(filename + '.tsl')
