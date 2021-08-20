#!/usr/bin/env python3

import subprocess
import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Simplified CC1 frontend')

parser.add_argument('--qinclude', action='append', help = 'Include Paths for iquote', required = False, dest='qinclude')
parser.add_argument('--binclude', action='append', help = 'Include Paths for Block Include', required = False, dest='binclude')
parser.add_argument('--cc1', action='store', help = '<Required> cc1 Path', required = False, dest='cc1')
parser.add_argument('--version', action='store', help = 'Get Version String of cc1', required = False, dest='version')
parser.add_argument('--preproc', action='store', help ='preproc path', required = False, dest='preproc')
parser.add_argument('--charmap', action='store', help ='preproc charmap', required = False)
parser.add_argument('-S', action='store_true', help='will be dropped', required = False, dest='as_only')

args, remainder = parser.parse_known_args()
'''
repopath = "/pretrepos/pokeemerald/"
agbccpath = "/agbcc_build/tools/"
agbcc = agbccpath+ "agbcc/bin/agbcc"
preproc = repopath+ "tools/preproc/preproc"
charmap = repopath+ "charmap.txt"
'''
if args.version:
    git_proc = subprocess.run(['git', '--git-dir='+args.version+'/.git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE)
    sys.stdout.write("pycc frontend for agbcc1 " + os.path.basename(args.version) + "@" + git_proc.stdout.decode('utf-8'))
    quit()
    
source = remainder[-1]
cpp_args = ["cpp", "-nostdinc", "-undef"]

# Add Block Includes and Quote Includes
if args.qinclude:
    for q in args.qinclude:
        cpp_args += ["-iquote", q]

if args.binclude:
    for b in args.binclude:
        cpp_args += ["-I", b]

cpp_args += [source, "-o", source+".i"]
subprocess.call(cpp_args)
if args.preproc and args.charmap:
    pprocess = subprocess.Popen([args.preproc, source+'.i', args.charmap], stdout=subprocess.PIPE)
    subprocess.call([args.cc1] + remainder[0:-1], stdin=pprocess.stdout)
else:
    with open(source+'.i', 'r') as a:
        subprocess.call([args.cc1] + remainder[0:-1], stdin=a)

if os.path.exists(source+'.i'):
    os.remove(source+'.i')
'''
source = sys.argv[-1]
subprocess.call(["cpp", "-nostdinc", "-undef", "-iquote", repopath + "include" , "-I", agbccpath + "agbcc", "-I", agbccpath + "agbcc/include", source, "-o", source+".i"])
pprocess = subprocess.Popen([preproc, source+".i", charmap], stdout=subprocess.PIPE)
subprocess.call([agbcc] + sys.argv[1:-1], stdin=pprocess.stdout)

if os.path.exists(source+".i"):
        os.remove(source+".i")
'''