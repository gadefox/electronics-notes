import sys
from pathlib import Path

def crc32(data):
  """Calculate CRC-32 (IEEE 802.3 polynomial)"""
  crc = 0xFFFFFFFF

  for byte in data:
    crc ^= byte
    for _ in range(8):
      crc = (crc >> 1) ^ (0xEDB88320 if crc & 1 else 0)
    
  return ~crc & 0xFFFFFFFF

if len(sys.argv) < 2:
  print(f"Usage: {sys.argv[0]} file")
  sys.exit(1)

path = Path(sys.argv[1])
if not path.exists():
  print(f"Error: file '{sys.argv[1]}' not found")
  sys.exit(1)
 
data = open(sys.argv[1], "rb").read()
crc = crc32(data) & 0xFFFFFFFF
print(f"CRC32: 0x{crc:08X}")
