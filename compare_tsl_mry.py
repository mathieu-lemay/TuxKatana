#!/usr/bin/env python3
import sys, re
import json
from lib.midi_bytes import Address, MIDIBytes

def checksum(body):
    """Checksum MIDI simple pour un bloc de bytes"""
    s = sum(body) % 128
    return MIDIBytes([(128 - s) % 128])

def load_tsl(tsl_file):
    with open(tsl_file, "r") as f:
        tsl = json.load(f)
    return tsl

def load_memory_dump(mry_file):
    with open(mry_file, "rb") as f:
        return f.read()

def main(tsl_file, mry_file):
    tsl = load_tsl(tsl_file)
    memory = load_memory_dump(mry_file)
    
    r_mem = " ".join(f"{x:02X}" for x in memory)
    # r_mem = s_mem.copy()
    # print(s_mem)
    for name, data in tsl['data'][0][0]['paramSet'].items():
        s_data = " ".join(data)
        res = None
        cks = checksum(MIDIBytes(s_data))
        if len(data) > 2 and cks.int != 0:
            if s_data in r_mem:
                res = r_mem.find(s_data)
            if res != None:
                pos = int(res/3) if res >0 else res
                print(f"✅ start: +{pos} =>",  
                      '\033[32;1m' + str(Address('60 00 00 00')+pos)+" -", 
                      '\033[36m' + name, 
                      '\033[35msize=' + str(len(data)) + '\033[0m', f"[{cks}]")
                print('>>>', s_data)
                pattern = r'\b' + re.escape(s_data) + r'\b'
                # replacement = '\033[31m'+' '.join(['XX'] * len(data))+'\033[0m'
                replacement = ' '.join(['XX'] * len(data))
                r_mem = re.sub(pattern, replacement, r_mem, count=1)
                if s_data in r_mem:
                    print("SECOND")
                # print(r_mem)
        else:
            # res = find( s_data, r_mem )
            print("⚠️ ", name, len(data), cks)
    print("Not Found zones :")
    for c in range(0, len(r_mem), 3):
        if r_mem[c:c+2] == 'XX':
            print('\033[30m', end='')
        elif r_mem[c:c+2] == '00':
            print('\033[31m', end='')
        else:
            print('\033[0m', end='')

        print(r_mem[c:c+3], end='')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <fichier.tsl> <dump_memory.bin>")
        sys.exit(1)
    _, tsl_file, mry_file = sys.argv
    main(tsl_file, mry_file)

