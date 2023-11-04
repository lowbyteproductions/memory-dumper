import sys
import re
import os

from ctypes import CDLL, c_ulong, c_long

c_ptrace = CDLL("libc.so.6").ptrace
c_ptrace.argtypes = (c_ulong, c_ulong, c_ulong, c_ulong)
c_ptrace.restype = c_long

PTRACE_ATTACH = c_ulong(16)
PTRACE_DETACH = c_ulong(17)

def ptrace(request, pid):
    c_pid = c_ulong(pid)
    return c_ptrace(request, c_pid, c_ulong(0), c_ulong(0))

maps_info_re = r"^([a-f0-9]+)\-([a-f0-9]+)\s(...)"

def read_maps_info(pid):
    filepath = f"/proc/{pid}/maps"
    with open(filepath) as f:
        maps_file = f.read()
    lines = maps_file.strip().splitlines()

    info_results = []

    for line in lines:
        result = re.match(maps_info_re, line)
        if result is None:
            raise Exception(f"Couldn't read map info on line: {line}")
        (start_addr, end_addr, perm) = result.groups()
        info_results.append((int(start_addr, 16), int(end_addr, 16), perm))

    return info_results

if len(sys.argv) < 2:
    print(f"usage: python {sys.argv[0]} <pid>")
    exit(1)

pid = sys.argv[1]

maps_info = read_maps_info(pid)

with open(f"dump-{pid}.bin", "wb") as df:
    ptrace(PTRACE_ATTACH, int(pid))
    with open(f"/proc/{pid}/mem", "rb") as mem:
        for start_addr, end_addr, perm in maps_info:
            if "r" in perm and "w" in perm:
                blob_len = end_addr - start_addr
                mem.seek(start_addr, os.SEEK_SET)
                blob = mem.read(blob_len)
                df.write(blob)
    ptrace(PTRACE_DETACH, int(pid))
