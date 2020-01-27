'''
Generate import graph as a DOT file.
'''
#!/usr/bin/env python3

import sys
import json
import tempfile
import os
import subprocess
import yaml

from semantic.graph import Graph

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

apk = os.path.realpath(sys.argv[1])
out = os.path.realpath(sys.argv[2])
depth = int(sys.argv[3])
filter_pkgs = []
preserve_pkgs = None
if len(sys.argv) > 4:
    arg = sys.argv[4]
    if arg.startswith("-"):
        filter_pkgs = arg[1:].split(",")
    elif arg.startswith("="):
        preserve_pkgs = arg[1:].split(",")

os.chdir(SCRIPT_DIR)

output_file = "tmp/" + os.path.basename(apk).replace(".apk", "") + "-callgraph.json"
if not os.path.exists(output_file):
    subprocess.check_output(["./liquid", apk, "callgraph.txt", output_file])

cfg = yaml.safe_load(open("config.yaml", "r").read())
pkg_prefixes = cfg["whitelistPackagePrefixes"]

bindings = json.loads(open(output_file, "r").read())

def class_pkg(clazz):
    for pkg in pkg_prefixes:
        if clazz.startswith(pkg):
            return pkg
    return ".".join(clazz.split(".")[:depth]).split("$")[0]

edges = []
for b in bindings:
    callee = class_pkg(b["gclass"])
    caller = class_pkg(b["C"])
    if callee is None or caller is None or callee == caller:
        continue
    edges.append((caller, callee))

g = Graph()
g.add_edges(edges)

to_kill = []
to_preserve = []
for node in g.nodes:
    if preserve_pkgs is not None:
        if all(not node.startswith(pkg) for pkg in preserve_pkgs):
            to_kill.append(node)
        else:
            to_preserve.append(node)
    else:
        for pkg in filter_pkgs:
            if node.startswith(pkg):
                to_kill.append(node)

print("Preserve: %s" % to_preserve)

for u, v in zip(to_preserve, to_preserve[1:]):
    print("Pathes between %s, %s" % (u, v))
    for p in g.get_all_paths(u, v):
        print("\t" + str(p))

print("Remove: %s" % to_kill)
g.remove_nodes_soft(to_kill)

with open(out, "w") as f:
    f.write("digraph {\n")
    for u, v in g.edges:
        f.write('"' + u + '" -> "' + v + '"\n')
    f.write("}\n")
