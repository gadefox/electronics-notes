import struct, sys
from pathlib import Path

if len(sys.argv) < 2:
  print(f"Usage: {sys.argv[0]} firmware")
  sys.exit(1)

path = Path(sys.argv[1])
if not path.exists():
  print(f"Error: file '{sys.argv[1]}' not found")
  sys.exit(1)

fw_seqnum = 0
with open(path, "rb") as f:
  while True:
    header = f.read(16)  # 4x DWORD = 16 bytes
    length = len(header)
    if length == 0:
      break
    if length < 16:
      print(f"⚠️invalid segment ({length} bytes)")
      break

    fw_seqnum += 1
    cmd, addr, length, crc = struct.unpack("<4I", header)
    if cmd == 1:
      print(f"{fw_seqnum} DNLD: addr=0x{addr:08X}({addr}) length={length} crc={crc:08X}")
    elif cmd == 4:
      print(f"{fw_seqnum} LAST: data1=0x{addr:08X}({addr}) data2=0x{addr:08X}({legth}) crc={crc:08X}")
      length = 0
    elif cmd == 6:
      print(f"{fw_seqnum} CMD6: data1=0x{addr:08X}({addr}) data2=0x{addr:08X}({legth}) crc={crc:08X}")
      length = 0
    elif cmd == 7:
      print(f"{fw_seqnum} CMD7: data1=0x{addr:08X}({addr}) data2={length:08X}({length}) crc={crc:08X}")
      length = 0
    elif cmd == 10:
      print(f"{fw_seqnum} CMD10: data1=0x{addr:08X}({addr}) data2={length:08X}({length}) crc={crc:08X}")
      length = 0
    elif cmd == 21:
      print(f"{fw_seqnum} CMD21: data1=0x{addr:08X}({addr}) data2={length:08X}({length}) crc={crc:08X}")
    else:
      print(f"⚠️{fw_seqnum}: cmd={cmd} addr=0x{addr:08X} length={length} crc={crc}")

    f.seek(length, 1)
