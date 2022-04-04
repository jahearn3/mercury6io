# Update param.in
#
# Author: Joseph A'Hearn
# Created 04/05/2017
#
# This program sets the specified value for the stop time
#

import sys

start_time = 0
simltn_yrs = float(sys.argv[1])
output_interval = float(sys.argv[2])
stop_time = start_time + (simltn_yrs * 365.25)

lines = open('param.in').readlines()
open('param.in', 'w').writelines(lines[0:7])
open('param.in', 'a').write(" stop time (days) = " + str(stop_time) + "\n")
open('param.in', 'a').write(" output interval (days) = " + str(output_interval) + "\n")
open('param.in', 'a').writelines(lines[9:37])