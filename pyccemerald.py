#!/usr/bin/env python3

import subprocess
import sys
import os

repopath = "/home/karathan/Dokumente/romhacking/sots/pokemon-sots/"
agbccpath = "/home/karathan/Dokumente/romhacking/sots/pokemon-sots/tools/"
agbcc = agbccpath+ "agbcc/bin/agbcc"
preproc = repopath+ "tools/preproc/preproc"
charmap = repopath+ "charmap.txt"

if sys.argv[1] == "-version":
    subprocess.call([agbcc, "-version"])

source = sys.argv[-1]
cpp_args = ["cpp", "-nostdinc", "-undef", "-iquote", repopath + "include" , "-I", agbccpath + "agbcc", "-I", agbccpath + "agbcc/include", source, "-o", source+".i"]
print(cpp_args)
subprocess.call(cpp_args)
pprocess = subprocess.Popen([preproc, source+".i", charmap], stdout=subprocess.PIPE)
subprocess.call([agbcc] + sys.argv[1:-1], stdin=pprocess.stdout)

if os.path.exists(source+".i"):
        os.remove(source+".i")
