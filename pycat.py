#!/usr/bin/env python3

import os
import argparse
import shutil
import re

parser = argparse.ArgumentParser(description='Simplified "compiler" frontend, cats any input')

parser.add_argument('--version', action='store_true', help = 'Get Version String of cc1', required = False, dest='version')
parser.add_argument('-o', action='store', help = 'Output Assembly file', required = False, dest='destination')
parser.add_argument('--no-parse', action='store_true', help = 'Do not parse the output', required = False, dest='no_parse')
parser.add_argument('-S', action='store_true', help='will be dropped', required = False, dest='as_only')
args, remainder = parser.parse_known_args()

if args.version:
    print("pycat frontend for cexplore")
    quit()

source = remainder[-1]

with open(source, 'r') as f_src, open(args.destination, 'w') as f_dst:
    for line in f_src:
        line2 = line
        if not args.no_parse:
            line2 = line.strip()
            if line2 and ':' not in line2 and not line2.startswith('@') and not line2.startswith('//'):
                instruction = line2.split(maxsplit=1)
                if len(instruction) > 1:
                    opcode, operand = instruction
                    if opcode.endswith('s') and (opcode.startswith('bic') or not opcode.startswith('b')): # exclude opcodes like bxcs/bls/biccs, but bics is fine
                        opcode = opcode[:-1]
                    rx_ry = re.search(r'r\d{1,2}-r\d{1,2}', operand, re.I)
                    if rx_ry:
                        rx_ry = rx_ry.group(0)
                        pos = rx_ry.find('-')
                        x = int(rx_ry[1:pos])
                        y = int(rx_ry[pos + 2:])
                        operands = operand.split(rx_ry, 1)
                        operand = operands[0]
                        for i in range(x, y + 1):
                            operand += 'r{}, '.format(i)
                        operand = operand[:-2] + operands[1]
                    dec_num = re.search(r'#\-?\d+', operand, re.I)
                    if dec_num:
                        dec_num = dec_num.group(0)
                        if dec_num[1] != '-':
                            value = int(dec_num[1:])
                            if value != 0:
                                s = operand.split(dec_num, 1)
                                operand = '{}#0x{:x}{}'.format(s[0], value, s[1])
                        else:
                            value = int(dec_num[2:])
                            if value != 0:
                                s = operand.split(dec_num, 1)
                                operand = '{}#-0x{:x}{}'.format(s[0], value, s[1])
                    if opcode in ('add', 'sub', 'lsl', 'lsr', 'asr', 'ror', 'and', 'orr', 'eor'):
                        operands = operand.split(',')
                        if len(operands) == 2:
                            operand = operands[0] + ', ' + operand
                    line2 = '\t{}\t{}'.format(opcode, operand)
        if not args.no_parse:
            f_dst.write(line2 + '\n')
        else:
            f_dst.write(line2)
