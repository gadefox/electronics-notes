import struct, sys
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

def info(msg: str):
  print(Fore.CYAN + " " + msg)

def warn(msg: str):
  print(Fore.YELLOW + " " + msg)

def error(msg: str):
  print(Fore.RED + "❌" + msg)

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

def main():
  if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} firmware")
    return

  path = Path(sys.argv[1])
  if not path.exists():
    error(f"File '{sys.argv[1]}' not found")
    return

  input = open(path, "rb")
  output = open(sys.argv[1] + ".payload", "wb")

  with open(path, "rb") as input:
    while True:
      header = input.read(16)  # 4x DWORD = 16 bytes
      length = len(header)
      if length == 0:
        break
      if length < 16:
        warn(f"Invalid segment ({length} bytes)")
        break

      crc = crc32(header)
      if crc != 0:
        warn(f"Header: invalid CRC (0x{crc:08X})")
        break

      cmd, addr, length, crc = struct.unpack("<4I", header)
      payload = input.read(length)
      if len(payload) < length:
        error(f"Expected {length} bytes but read {len(payload)}.")
        break
      if crc32(payload):
        error("Payload: invalid CRC.")
        break

      payload = payload[:-4]
      output.write(payload)

  output.close()

main()
