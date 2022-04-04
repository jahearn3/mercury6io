# Update element.in
#
# Author: Joseph A'Hearn
# Created 06/17/2020
#
# This program sets the minimum interval between outputs
#

import sys

output_interval = float(sys.argv[1]) # in days

lines = open('element.in').readlines()
open('element.in', 'w').writelines(lines[0:9])
open('element.in', 'a').write(" minimum interval between outputs (days) = " + str(output_interval) + "\n")
open('element.in', 'a').writelines(lines[10:18])