import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio #GLib, Gdk, GObject
import os

import logging
from lib.log_setup import LOGGER_NAME
log = logging.getLogger(LOGGER_NAME)

class FileChooser(Gtk.FileChooserDialog):
    def __init__(self, win, parent, title="Choose Preset file",
                 action=Gtk.FileChooserAction.OPEN):#,
        self.parent= parent
        super().__init__(title=title, transient_for=win, action=action)

        self.set_modal(True)
        cwd = os.getcwd()
        self.set_current_folder(Gio.File.new_for_path(cwd+"/presets"))

    def add_filter(self, name, patterns):
        f = Gtk.FileFilter()
        f.set_name(name)
        for p in patterns:
            f.add_pattern(p)
        Gtk.FileChooserNative.add_filter(self, f)

    def choose(self, callback):
        def on_response(dialog, response):
            file_path = None
            if response == Gtk.ResponseType.ACCEPT:
                file = dialog.get_file()
                if file:
                    file_path = file.get_path()
                    log.debug(f"{file_path}")
                    callback(file_path)
                    # dialog.parent.file_path = file_path
                    # dialog.parent.filename.set_text(os.path.basename(file_path).split('.')[0])
            dialog.destroy()

        self.connect("response", on_response)
        self.show()
 
