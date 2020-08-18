#!/usr/bin/env python3

"""
Main.
Runs the cpu
"""


import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()