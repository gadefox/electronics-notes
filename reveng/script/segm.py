import os, subprocess, sys

src="flash.bin"

if len(sys.argv) < 2:
  print(f"Usage: {sys.argv[0]} <offset1> <offset2> ...")
  sys.exit(1)

offsets_hex = sys.argv[1:]
offsets = [int(x,16) for x in offsets_hex]
offsets.sort()  # sort just in case

outdir="segm"
os.makedirs(outdir, exist_ok=True)

for i, start in enumerate(offsets):
  if i < len(offsets)-1:
    size = offsets[i+1] - start
  else:
    size = None  # to EOF

  outname = os.path.join(outdir, f"{start:08x}")
  if size:
    print(f"Extracting {outname}: start=0x{start:08x} ({start}), size=0x{size:x} ({size})")
    # use dd but faster with bs=4096 (calculate skip/count in blocks)
    bs=4096
    skip = start // bs
    skip_rem = start % bs
    if skip_rem == 0:
      count = size // bs
      subprocess.run(["dd", "if="+src, "of="+outname, f"bs={bs}", f"skip={skip}", f"count={count}"])
    else:
      # fallback to bytewise for unaligned: slower but safe
      subprocess.run(["dd","if="+src,"of="+outname,f"bs=1","skip="+str(start),"count="+str(size)])
  else:
    print(f"Extracting last {outname}: start=0x{start:08x} ({start}) to EOF")
    subprocess.run(["dd","if="+src,"of="+outname,f"bs=1","skip="+str(start)])
