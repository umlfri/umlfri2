#!/bin/bash

inkscape ../logo/logo_small.svg -z -C -w 16 -h 16 --export-png=16.png
inkscape ../logo/logo_full.svg -z -C -w 32 -h 32 --export-png=32.png
inkscape ../logo/logo_full.svg -z -C -w 64 -h 64 --export-png=64.png
inkscape ../logo/logo_full.svg -z -C -w 128 -h 128 --export-png=128.png

convert 16.png 32.png 64.png 128.png icon.ico

rm *.png
