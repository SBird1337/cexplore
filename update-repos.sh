#!/bin/sh

cd /pretrepos/pokeemerald && git pull && make tools
cd /pretrepos/pokefirered && git pull && make tools
cd /pretrepos/pokeruby && git pull && make tools