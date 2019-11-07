from pynrfjprog import API, Hex
import os
from pyfiglet import Figlet

f = Figlet(font='slant')
print(f.renderText('Binary Flasher'))
print("# Flashing .hex FW")

# Where to look for flashable .hex files (default current dir)
#directory = "."
directory = "//media//charles/Data//SDK/Release//pca10040/build//"

fw_file = [fname for fname in os.listdir(directory)
           if fname.endswith('.hex')]

for item in enumerate(fw_file):
    print("[%d] %s" % item)
try:
    fw = int(input("\nSelect number to flash: "))
except ValueError:
    print("Please select a number")
try:
    chosen = fw_file[fw]
except IndexError:
    print("Please select valid number")

print("\n# Looking for Nordic Device")
with API.API(API.DeviceFamily.UNKNOWN) as api:
    api.connect_to_emu_without_snr()
    device_family = api.read_device_family()

api = API.API(device_family)
api.open()
api.connect_to_emu_without_snr()

print("# Found " + device_family + " device with serial: " + api.read_connected_emu_snr().__str__())
test = api.is_connected_to_emu()
if test is True:
    print("# Connection is established")
else:
    print("not connected")
    exit()

print("# Erasing Flash")
api.recover()
module_dir = directory
# module_file = chosen

# module_dir, module_file = os.path.split(__file__)

directory, chosen = os.path.split(__file__)
hex_file_path = os.path.join(os.path.abspath(module_dir), fw_file[fw])

print("# Parsing hex file into segments")
fw3_2 = Hex.Hex(hex_file_path)

print('# Writing %s to device.' % hex_file_path)
for segment in fw3_2:
    api.write(segment.address, segment.data, True)

api.sys_reset()
api.pin_reset()
api.go()
api.close()
print("# All done...")
