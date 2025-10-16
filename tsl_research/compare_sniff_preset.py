from lib.midi_bytes import MIDIBytes, Address
import re
msg=[]
def checksum(body):
    s = sum(body) % 128
    return MIDIBytes([(128 - s) % 128])

msgs = {}
mry=""
import json
tsl = {}
with open("James_read.json", 'r') as f:
    tsl = json.load(f)
with open("mry_snif.txt", 'r') as f:
    mry = f.readlines()
mry = mry[0]
# print(tsl)
# print(mry)
for name, data in tsl.items():
    cks = checksum(MIDIBytes(data))
    res = None
    # print(name, len(data.split()), cks.int)
    if len(data.split())>2 and cks.int != 0:
        res = mry.find(data.lower())
        # print(res)
        if res != None:
            pos = int(res/3) if res >0 else res
            print(f"✅ start: +{pos} =>",  
                  '\033[32;1m' + str(Address('60 00 00 00')+pos)+" -", 
                  '\033[36m' + name, 
                  '\033[35msize=' + str(len(data.split())) + '\033[0m', f"[{cks}]")
            pattern = r'\b' + re.escape(data) + r'\b'
            replacement = ' '.join(['XX'] * len(data))
            mry = re.sub(pattern, replacement, mry, count=1)
    else:
        # res = find( s_data, r_mem )
        print("⚠️ ", name, len(data), cks)
print(mry)
        # idx =
        # print(name,'>>', Address('60 00 00 00')+idx)
# print(tsl['UserPatch%Patch_0'])
# print(tsl['UserPatch%PatchName'])
# def form_msg():
# for m in msg:
#     octs = [m[i:i+2] for i in range(0, len(m), 2)]
#     filtered = [b for i, b in enumerate(octs) if (i % 4) != 0]
#     res = ' '.join(filtered)
#     res = res.replace('f0 41 00 00 00 00 33 12 ','').replace(' f7 00 00', '')
#     res = res[:-3]
#     addr = res[:11]
#     data = res[12:]
#     msgs[addr] = data
#     mry += data+' '

# def show():
#     count = 0
#     for addr, data in msgs.items():
#         size = len(data.split())
#         count += size
#         print(f"\033[34;1m{addr}: \033[32m{data}\033[0m ({size})")
#         print(Address(addr) + size)
#         print('-'*10)
#     print(f"Total: {count}")
# show()
# with open("mry_snif.txt", 'w') as f:
    # f.write(mry)
# print(mry)

# for name, data in tsl.items():
    # data = " ".join(data)
    # tsl[name] = data
# for name, data in tsl.items():
    
    # print(k, v)

# with open("James_read.json", 'w') as f:
    # json.dump( tsl, f )


