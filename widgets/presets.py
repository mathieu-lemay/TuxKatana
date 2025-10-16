import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gdk, GObject

import logging
from lib.log_setup import LOGGER_NAME
log = logging.getLogger(LOGGER_NAME)

from .preset import PresetUI


# class PresetEntry(Gtk.Entry):
#     def __init__(self, text):
#         super().__init__()
#         self.name = text
#         self.set_text(text)
#         self.test='coucou'

class PresetRow(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        # self.channel_idx = -1
        self.chan = Gtk.Label(xalign=1)
        self.name = Gtk.Label()

        self.append(self.chan)
        self.append(self.name)

class PresetsPage(Gtk.Box):
    selected = GObject.Property(type=int, default=-1)
    def __init__(self, ctrl):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.ctrl = ctrl
        # self.own_ctrl = self.ctrl.presets

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self.on_setup)
        factory.connect("bind", self.on_bind)

        # self.selection = Gtk.SingleSelection.new(ctrl.presets)
        self.selection = Gtk.MultiSelection.new(ctrl.presets)
        listview = Gtk.ListView.new(self.selection, factory)
        listview.get_style_context().add_class('inner')
        self.append(listview)

        self.preset_ui = PresetUI(self, ctrl)
        self.append(self.preset_ui)

        self.selected_channels = []

        self.selection.connect("selection-changed", self.on_selection_changed)
        self.ctrl.mry.connect('mry-loaded', self.on_mry_loaded)
        self.ctrl.connect("channel-changed", self.on_channel_changed)

    def on_channel_changed(self, obj, ch_num):
        self.selection.select_item(ch_num - 1, True)
        self.preset_ui.chan_sel.set_active_id(str(ch_num-1))

    def on_mry_loaded(self, mry):
        preset_name = self.ctrl.mry.get_actual_preset()
        index = self.find_index(self.selection, preset_name)
        self.ctrl.emit("channel-changed", int(index+1))

    def on_selection_changed(self, selection, position, n_items):
        bitset = selection.get_selection()
        model = selection.get_model()
        self.selected_channels = [model.get_item(i) \
            for i in range(model.get_n_items()) \
            if bitset.contains(i)]
        sel_itms = self.selected_channels
        if len(sel_itms) == 1:
            self.preset_ui.chan_sel.set_active_id(str(sel_itms[0].chan-1))
        log.debug([(si.chan,si.name) for si in self.selected_channels])

    def find_index(self, selection, name):
        model = selection.get_model()
        for i in range(model.get_n_items()):
            itm = model.get_item(i)
            if name.strip() == itm.name.strip():
                return i
        return 0

    def on_setup(self, factory, list_item):
        row = PresetRow()
        list_item.set_child(row)

    def on_bind(self, factory, list_item):
        row: PresetRow = list_item.get_child()
        preset: Preset = list_item.get_item()
        preset.bind_property(
            "chan",
            row.chan,
            "label",
            GObject.BindingFlags.SYNC_CREATE,
            transform_to=lambda _b, n: f"CH_{n}:",
        )
        preset.bind_property(
            "name",
            row.name,
            "label",
            GObject.BindingFlags.SYNC_CREATE
        )


