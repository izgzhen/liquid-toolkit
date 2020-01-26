'''
Generate import graph as a DOT file.
'''
#!/usr/bin/env python3

import sys
import json
import tempfile
import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

apk = os.path.realpath(sys.argv[1])
out = os.path.realpath(sys.argv[2])
depth = int(sys.argv[3])

os.chdir(SCRIPT_DIR)

tmp = tempfile.NamedTemporaryFile(delete=False).name
subprocess.check_output(["./liquid", apk, "callgraph.txt", tmp])

bindings = json.loads(open(tmp, "r").read())

added_links = set()

def class_pkg(clazz):
    return ".".join(clazz.split(".")[:depth])

with open(out, "w") as f:
    f.write("digraph {\n")
    for b in bindings:
        callee = '"' + class_pkg(b["gclass"]) + '"'
        caller = '"' + class_pkg(b["C"]) + '"'
        if callee == caller:
            continue
        link = callee + " -> " + caller
        if link not in added_links:
            added_links.add(link)
            f.write(link + "\n")
    f.write("}\n")
