#!/usr/bin/env python3

import subprocess
import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Simplified "compiler" frontend, cats any input')

parser.add_argument('--version', action='store_true', help = 'Get Version String of cc1', required = False, dest='version')

args, remainder = parser.parse_known_args()

if args.version:
    print("pycat frontend for cexplore")
    quit()
    
source = remainder[-1]
f = open(source, "r")
print(f.read())
f.close()