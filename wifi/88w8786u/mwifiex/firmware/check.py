import struct, sys
from pathlib import Path

def crc32(data: bytes) -> int:
  crc = 0
  for byte in data:
    crc ^= byte << 24
    for _ in range(8):
      if crc & 0x80000000:
        crc = ((crc << 1) ^ 0x04C11DB7) & 0xFFFFFFFF
      else:
        crc = (crc << 1) & 0xFFFFFFFF
  return crc

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
    if crc32(header) != 0:
      print("⚠️header: invalid CRC")
      break

    fw_seqnum += 1
    cmd, addr, length, crc = struct.unpack("<4I", header)
    if cmd == 4:
      if addr != 0:        print(f"⚠️invalid addr value: {addr}")
      if length != 0:      print(f"⚠️invalid length value: {length}")
      if crc != 411884319: print(f"⚠️invalid crc value: {crc}")
      print(f"{fw_seqnum} LAST")
      continue
    if cmd == 6:
      if length != 0:      print(f"⚠️invalid length value: {length}")
      print(f"{fw_seqnum} CMD6: data=0x{addr:08X}({addr}) crc=0x{crc:08X}")
      continue
    if cmd == 7:
      if addr != length:   print(f"⚠️invalid addr ({addr}) and length ({length}) values")
      print(f"{fw_seqnum} CMD7: data={addr} crc=0x{crc:08X}")
      continue
    if cmd == 1:
      print(f"{fw_seqnum} DNLD: addr=0x{addr:08X}({addr}) length={length} crc=0x{crc:08X}")
    else:
      print(f"⚠️{fw_seqnum}: cmd={cmd} addr=0x{addr:08X}({addr}) length={length} crc=0x{crc}")

    payload = f.read(length)
    if crc32(payload) != 0:
      print("⚠️payload: invalid CRC")
      break
