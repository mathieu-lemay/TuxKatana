import json
from ruamel.yaml import YAML
yaml = YAML(typ="rt")
from lib.midi_bytes import Address, MIDIBytes
from termcolor import colored as color
with open("sniff.txt", 'r'):
    
tsl = {}
with open("James_read.json", 'r') as f:
    tsl = json.load(f)

with open("params/presets_addrs.yaml", 'r') as f:
    mapping = yaml.load(f)

start = None
count = 0
mry = MIDIBytes()
for name in mapping:
    addr, size = mapping[name].values()
    addr = Address(addr)
    if not start:
        start = addr
    data = MIDIBytes( tsl[name] )
    print(f"{name}: {addr} ({size}) <<< {start+len(mry)}")
    if start+len(mry) == addr:
        print(color(f">>> {name}", 'green')+ f": {addr} ({size})")
        mry += data
    elif addr:
        # print(f"{addr-start-len(mry)} {size}")
        diff = addr - (start+len(mry))
        # print(diff)
        add = MIDIBytes('00 '*diff)
        mry += data + add
        print(f"{len(data)=}  {size=} {addr=} {start+len(mry)=}")
    count += len(data)
    # print(addr, data, len(data))
print(mry, len(mry))
