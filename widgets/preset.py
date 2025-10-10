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
    def __init__(self, own_ctrl):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # self.set_hexpand(False)
        self.own_ctrl = own_ctrl
        self.filename = None
        self.file_path = None
        self.selected_channel = None

        # h_box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        # # label = Gtk.Label(label="Filename: ")
        # # h_box1.append(label)
        # writechan = Gtk.Button(label="Write to Amp")
        # writechan.connect("clicked", self.on_load_clicked)
        # h_box1.append(writechan)
        # self.append(h_box1)

        # 📂 ⬆️  ⬇️  ✅
        

        box_tsl = BoxInner(label="TSL File", h_box=True)
        box_tsl.set_spacing(6)

        # box_tsl.h_box.set_hexpand(True)
        self.append(box_tsl)

        self.reload = Gtk.Button(label="🔄")
        box_tsl.h_box.append(self.reload)
        # self.reload.set_halign(Gtk.Align.END)
        # self.reload.get_style_context().add_class('edit-mode')
        self.reload.set_tooltip_text("Reload Preset")
        # self.reload.connect("toggled", self.toggle_edit_mode)


        self.file = Gtk.Entry()
        self.file.set_hexpand(True)
        box_tsl.h_box.append(self.file)
        ext = Gtk.Label(label=".tsl   ")
        box_tsl.h_box.append(ext)

        self.save = Gtk.Button(label="💾")
        box_tsl.h_box.append(self.save)
        # self.save.set_halign(Gtk.Align.END)
        # self.save.get_style_context().add_class('edit-mode')
        self.save.set_tooltip_text("Save To TSL")
        # self.save.connect("toggled", self.toggle_edit_mode)

        self.open = Gtk.Button(label="📂")
        box_tsl.h_box.append(self.open)
        # self.save.set_halign(Gtk.Align.END)
        # self.save.get_style_context().add_class('edit-mode')
        self.open.set_tooltip_text("Open TSL")
        # self.save.connect("toggled", self.toggle_edit_mode)

        box = BoxInner(label="TSL Contained Presets", h_box=True)
        box.set_spacing(6)
        self.append(box)

        self.select = Gtk.ComboBoxText()
        self.select.set_hexpand(False)
        self.open.set_tooltip_text("Select Contained Preset")
        box.h_box.append(self.select)

        self.load = Gtk.Button(label="⬆️ ")
        box.h_box.append(self.load)
        self.load.set_halign(Gtk.Align.END)
        # self.save.get_style_context().add_class('edit-mode')
        self.save.set_tooltip_text("Save To TSL")
        # self.save.connect("toggled", self.toggle_edit_mode)


#         savefile = Gtk.Button(label="Save")
#         savefile.set_halign(Gtk.Align.END)
#         savefile.connect("clicked", self.on_save_clicked)
#         box_tsl.h_box.append(savefile)

#         selectfile = Gtk.Button(label="Select")
#         selectfile.set_halign(Gtk.Align.END)
#         selectfile.connect("clicked", self.on_select_clicked)
#         box_tsl.h_box.append(selectfile)

    def on_select_clicked(self, widget):
        win = self.own_ctrl.device.ctrl.parent.win
        chooser = FileChooser(win, parent=self, title="Open .tsl file")
        chooser.add_filter("TSL Files", ["*.tsl"])
        chooser.add_buttons(
            "_Cancel", Gtk.ResponseType.CANCEL,
            "_Open", Gtk.ResponseType.ACCEPT
        )
        file_path = chooser.choose()
        log.debug(file_path)
        if self.file_path:
            self.filename = os.path.basename(self.file_path).split('.')[0]
            self.file.set_text(self.filename)

    def on_load_clicked(self, button):
        win = self.own_ctrl.device.ctrl.parent.win
        win.set_sensitive(False)
        ch_chooser = ChannelChooser(win, self)
        ch_chooser.connect("response", self.on_channel_choosed)
        ch_chooser.show()

    def on_channel_choosed(self, dialog, response):
        win = self.own_ctrl.device.ctrl.parent.win
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
        self.own_ctrl.save(filename + '.tsl')
