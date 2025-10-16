import os
import json

from gi.repository import GLib, GObject, Gio

from ruamel.yaml import YAML
yaml = YAML(typ="rt")

from .midi_bytes import MIDIBytes, Address

import logging
from lib.log_setup import LOGGER_NAME
log = logging.getLogger(LOGGER_NAME)

class TSLParser:#(GObject.GObject):
    # __gsignals__ = {
    #     "modfx-map-ready": (GObject.SIGNAL_RUN_FIRST, None, (object,object,)),
    # }
    def __init__(self, ui=None):
        # super().__init__()
        self.ui = ui
        # with open("params/format_preset.yaml", 'r') as f:
        with open("params/presets_addrs.yaml", 'r') as f:
            self.map = yaml.load(f)
        self.data={}
        self.revision = "0002"              # seem to tell the "UserPatch%Patch_Mk2V2" presence
        self.memo = ""
        self.path = os.getcwd() + "/presets"

    def open(self, file_path):
        self.file_path = file_path

        with open(file_path, 'r') as f:
            data = json.load(f)
        if data['device'] != "KATANA MkII":
            log.warning(f"{data['device']} != 'KATANA MkII'") # TODO : Alert Dialog
            return
        self.tsl_name = data['name']
        self.revision = data['formatRev']
        self.device = data['device']
        presets_list = data['data'][0]
        self.presets_list = {}
        self.ui.select.remove_all()
        for i, preset in enumerate(presets_list):
            frm = " ".join(preset['paramSet']['UserPatch%PatchName'])
            name = MIDIBytes(frm).to_chars().strip()
            self.presets_list[name] = preset
            self.ui.select.append(str(i), name)
        self.ui.select.set_active_id('0')

    def get_user_patches(self, name):
        log.debug(name)
        mry = {}
        if self.presets_list:
            for patch, data in self.presets_list[name]['paramSet'].items():
                mp = self.map[patch]
                log.debug(f"{patch} {data}")
                addr = Address(mp['addr'])
                # size = mp['size']
                frm = " ".join(data)
                data = MIDIBytes(frm)
                mry[addr] = data
            # log.debug(self.presets_list[name])
        return mry

    def generate(self):
        tsl = {}
        tsl['name'] = self.preset_name
        tsl['formatRev'] = self.revision
        tsl['device'] = self.device_name.replace('2', 'II')
        tsl['data'] = [[]]
        tsl['data'][0].append({})
        infos = tsl['data'][0][0]
        infos['memo'] = { 'memo': self.memo, "isToneCentralPatch": True}
        infos['paramSet'] = {}
        ps = infos['paramSet']
        offset = 0
        old_Addr = self.device.mry.Addr_start
        old_size = 0
        for k, vals in self.map.items():
            #log.debug(f"{to_str(self.device.mry.offset_to_addr(offset))=}")
            Addr = self.device.mry.Addr_start
            offset += vals['offset']
            Addr += offset
            old_Addr = Addr - old_size
            #log.debug(f"{old_Addr} = {Addr} - {old_size}")
            old_size = vals['size']
            #log.debug(f"{Addr} / size:{vals['size']} ofs:{vals['offset']}")
            data = self.device.mry.read(Addr, vals['size'], True).upper().split(' ')
            log.debug(f"{k}:> '{Addr}': {len(data)} {vals['offset']}")
            if len(data) < vals['size']:
                log.debug(data)
            ps[k] = self.device.mry.read(Addr, vals['size'], True).upper().split(' ')
            offset += vals['size']
        # log.debug(tsl)
        return tsl

    def save(self, filename="test.tsl"):
        self.filename = filename
        file_path = self.dir_path + '/' + filename
        with open(file_path, 'w') as f:
            json.dump(self.generate(), f)
        log.info(f"Preset saved to: {file_path}")


