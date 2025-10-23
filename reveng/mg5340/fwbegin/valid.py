import struct, sys

fw_seqnum = 0
with open("segm.bin", "rb") as f:
  while True:
    header = f.read(16)  # 4x DWORD = 16 bytes
    length = len(header)
    if length == 0:
      break
    if length < 16:
      break

    fw_seqnum += 1
    cmd, addr, length, crc = struct.unpack("<4I", header)
    if cmd == 4:
      print("ok")
      length = 0
    elif cmd in (6, 7, 10):
      length = 0

    f.seek(length, 1)
