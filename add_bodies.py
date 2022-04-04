# Add Bodies
#
# Author: Joseph A'Hearn
# Created 06/22/2017
#
# This program provides functions to get info about the bodies from the mercury6 input files
#   

import numpy as np 
import random
from constants_of_mercury6 import G, AU, M_Sun
from geo2xyz import geo2xyz
from useful import rawcount
import bodies as bd 


def assign_body_name(filename="big.in", named_bodies=0):
	line_count = rawcount(filename)
	body_count = int((line_count - 6) / 4)
	if((line_count - 6) % 4 == 3):
		body_count += 1
	numbered_bodies = body_count - named_bodies
	if(numbered_bodies < 9):
		body_name = "body000" + str(body_count + 1)
	elif(numbered_bodies < 99):
		body_name = "body00" + str(body_count + 1)
	elif(numbered_bodies < 999):
		body_name = "body0" + str(body_count + 1)
	else:
		body_name = "body" + str(body_count + 1)
	return body_name

def assign_mass(coefficient=3.0, exponent=20):
	coefficient = random.uniform(1, 9.9)
	exponent = random.randint(19, 23)
	return str(coefficient) + "d-" + str(exponent)

def new_body(filename="big.in", named_bodies=2, mass=0, coefficient=3.0, exponent=20):
	line_count = rawcount(filename)
	with open(filename, "a") as myfile:
		if((line_count - 6) % 4 == 3):
			myfile.write("\n")
		if((line_count - 6) % 4 != 1): # otherwise this function was probably just called
			body_name = assign_body_name(filename, named_bodies)
			if(mass == 0):
				m = assign_mass(coefficient, exponent)
			else:
				m = str(mass)
				m = m.translate({ord(j):'d' for j in 'e'})
			myfile.write(" " + str(body_name) + "   m=" + m + "\n")

def add_new_body(a=-1, e=1, i=360, mean_longitude=360, longit_perictr=360, long_ascnode=360, mass=0, coefficient=3.0, exponent=20):
	# default values are meant to be somewhat non-sensical to emphasize that they must be redefined
	new_body(mass, coefficient, exponent)
	# if input orbital elements have not been provided, set some of them randomly within a certain range
	#   in order that successive new bodies added do not occupy the same location
	if(a == -1):
		#a = random.uniform(167515.0, 167560.0)
		a = random.uniform(167500.0, 167513.0)
	if(e == 1):
		e = random.uniform(0.00001, 0.0008)
	if(i == 360):
		i = random.uniform(0.00001, 0.0917)
	if(mean_longitude == 360):
		#mean_longitude = random.uniform(195.0, 225.0)
		mean_longitude = random.uniform(202.0, 217.8)
	if(longit_perictr == 360):
		longit_perictr = random.uniform(0.0, 360.0)
	if(long_ascnode == 360):
		long_ascnode = random.uniform(0.0, 360.0)
	output_state_vectors(a, e, i, mean_longitude, longit_perictr, long_ascnode)

def output_state_vectors(a=-1, e=1, i=360, mean_longitude=360, longit_perictr=360, long_ascnode=360):
	with open("big.in", "a") as myfile:
		x_AU, y_AU, z_AU, u_AU, v_AU, w_AU = geo2xyz(a, e, i, mean_longitude, longit_perictr, long_ascnode)
		myfile.write("  " + str("{:.11e}".format(x_AU)) + " " + str("{:.11e}".format(y_AU)) + " " + str("{:.11e}".format(z_AU)) + "\n  " + str("{:.11e}".format(u_AU)) + " " + str("{:.11e}".format(v_AU)) + " " + str("{:.11e}".format(w_AU)) + "\n  0. 0. 0.")

def output_state_vectors_xyz(x, y, z, u, v, w):
	with open("big.in", "a") as myfile:
		x_AU, y_AU, z_AU, u_AU, v_AU, w_AU = km2AU(x, y, z, u, v, w)
		myfile.write("  " + str("{:.11e}".format(x_AU)) + " " + str("{:.11e}".format(y_AU)) + " " + str("{:.11e}".format(z_AU)) + "\n  " + str("{:.11e}".format(u_AU)) + " " + str("{:.11e}".format(v_AU)) + " " + str("{:.11e}".format(w_AU)) + "\n  0. 0. 0.")

def output_state_vectors_raw(x_AU, y_AU, z_AU, u_AU, v_AU, w_AU):
	with open("big.in", "a") as myfile:
		myfile.write("  " + str("{:.11e}".format(x_AU)) + " " + str("{:.11e}".format(y_AU)) + " " + str("{:.11e}".format(z_AU)) + "\n  " + str("{:.11e}".format(u_AU)) + " " + str("{:.11e}".format(v_AU)) + " " + str("{:.11e}".format(w_AU)) + "\n  0. 0. 0.")

def km2AU(x, y, z, u, v, w):
	b = 1.0E+03 / AU() 	# converts from km to AU
	c = b * 8.64E+04 	# converts from km/s to AU/day
	return x * b, y * b, z * b, u * c, v * c, w * c

def name_and_GM(name, GM):
	line_count = rawcount("big.in")
	while(len(name) < 8):
		name += ' '
	with open("big.in", "a") as myfile:
		if((line_count - 6) % 4 == 3):
			myfile.write("\n")
		if((line_count - 6) % 4 != 1): # otherwise this function was probably just called
			myfile.write(" " + str(name) + "   m=" + str("{:.11e}".format(GM / (G() * M_Sun()))) + "\n")

def add_satellite(name, GM, x, y, z, u, v, w):
	name_and_GM(name, GM * 1.0E+09)
	output_state_vectors_xyz(x, y, z, u, v, w)

def add_aeg_at_cer_contour(delta_lambda=0):
	#a = 167538
	a = 167506.5
	e = 0.000457806317
	i = 0.001319397343
	mean_longitude = 209.9 - delta_lambda
	longit_perictr = 157.983521
	long_ascnode = 319.6712727
	output_state_vectors(a, e, i, mean_longitude, longit_perictr, long_ascnode)

def add_aeg_at_exact_cer():
	with open("big.in", "a") as myfile:
		myfile.write("  " + 
			str("{:.11e}".format(-9.69202376624e-04)) + " " + 
			str("{:.11e}".format(-5.60505582316e-04)) + " " + 
			str("{:.11e}".format(-2.42837587635e-08)) + "\n  " + 
			str("{:.11e}".format(4.35545320095e-03))  + " " + 
			str("{:.11e}".format(-7.53752031756e-03)) + " " + 
			str("{:.11e}".format(-6.76283997543e-08)) + "\n  0. 0. 0.")

def remove_all():
	lines = open('big.in').readlines()
	open('big.in', 'w').writelines(lines[0:6])

def flat_circular_orbit(orbital_radius, mu2):
	mu1 = bd.central_body()[1]
	output_state_vectors(orbital_radius, 0, 0, 0, np.sqrt(G() * (mu1 + mu2) / (orbital_radius)), 0)

def remove_aeg_elements():
	lines = open('big.in').readlines()
	open('big.in', 'w').writelines(lines[0:11])

def a_body(m=1.0E-17):
	body_name = assign_body_name()
	with open('big.in', 'a') as myfile:
		if(body_name == 'body0001'):
			myfile.write(str(body_name) + "   m=" + str(m) + "\n")
		else:
			myfile.write("\n " + str(body_name) + "   m=" + str(m) + "\n")


def add_a_body(a=-1, e=1, i=360, mean_longitude=360, longit_perictr=360, long_ascnode=360, mass=1.0E-17):
	# default values are meant to be somewhat non-sensical to emphasize that they must be redefined
	a_body(mass)
	# if input orbital elements have not been provided, set some of them randomly within a certain range
	#   in order that successive new bodies added do not occupy the same location
	if(a == -1):
		#a = random.uniform(167515.0, 167560.0)
		a = random.uniform(167500.0, 167513.0)
	if(e == 1):
		e = 0.000457806317
	if(i == 360):
		i = 0.001319397343
	if(mean_longitude == 360):
		#mean_longitude = random.uniform(195.0, 225.0)
		mean_longitude = random.uniform(202.0, 217.8)
	if(longit_perictr == 360):
		longit_perictr = 157.983521
	if(long_ascnode == 360):
		long_ascnode = 319.6712727
	output_state_vectors(a, e, i, mean_longitude, longit_perictr, long_ascnode)

def add_body_randomly_in_ellipse(a=-1, e=1, i=360, mean_longitude=360, longit_perictr=360, long_ascnode=360, mass=0, coefficient=3.0, exponent=20):
	a_body()
	# if input orbital elements have not been provided, set some of them randomly within a certain range
	#   in order that successive new bodies added do not occupy the same location
	a_cer = 167506.5
	a_diff_max = 33.5
	l_cer = 209.9
	if(a == -1):
		a = random.uniform(a_cer - a_diff_max, a_cer + a_diff_max)
	if(e == 1):
		e = random.uniform(0.00001, 0.0008)
	if(i == 360):
		i = random.uniform(0.00001, 0.0917)
	if(mean_longitude == 360):
		a_diff = np.absolute(a - a_cer)
		l_span = (25 * (1 - ((a_diff / a_diff_max)**6))) + (5 * np.exp(-3 * a_diff / a_diff_max))
		mean_longitude = random.uniform(l_cer - l_span, l_cer + l_span)
	if(longit_perictr == 360):
		longit_perictr = random.uniform(0.0, 360.0)
	if(long_ascnode == 360):
		long_ascnode = random.uniform(0.0, 360.0)
	output_state_vectors(a, e, i, mean_longitude, longit_perictr, long_ascnode)

def Obj5_trailing_D68_configuration(a_perturbation=0, lambda_perturbation=0):
	add_a_body(67627 + (a_perturbation * random.uniform(-1, 1)), 0, 0,  90.000 + (lambda_perturbation * random.uniform(-1, 1)), 0, 0) # Object 5 trailing
	add_a_body(67627 + (a_perturbation * random.uniform(-1, 1)), 0, 0, 122.000 + (lambda_perturbation * random.uniform(-1, 1)), 0, 0) # Clump T
	add_a_body(67627 + (a_perturbation * random.uniform(-1, 1)), 0, 0, 148.000 + (lambda_perturbation * random.uniform(-1, 1)), 0, 0) # Clump M
	add_a_body(67627 + (a_perturbation * random.uniform(-1, 1)), 0, 0, 180.000 + (lambda_perturbation * random.uniform(-1, 1)), 0, 0) # Clump L
	add_a_body(67627 + (a_perturbation * random.uniform(-1, 1)), 0, 0, 209.000 + (lambda_perturbation * random.uniform(-1, 1)), 0, 0) # Clump LL

def Obj5_leading_D68_configuration(a_perturbation=0, lambda_perturbation=0):
	#add_a_body(67627 + (a_perturbation * random.uniform(-1, 1)), 0, 0, 122.000 + (lambda_perturbation * random.uniform(-1, 1)), 0, 0) # Clump T
	#add_a_body(67627 + (a_perturbation * random.uniform(-1, 1)), 0, 0, 148.000 + (lambda_perturbation * random.uniform(-1, 1)), 0, 0) # Clump M
	#add_a_body(67627 + (a_perturbation * random.uniform(-1, 1)), 0, 0, 180.000 + (lambda_perturbation * random.uniform(-1, 1)), 0, 0) # Clump L
	#add_a_body(67627 + (a_perturbation * random.uniform(-1, 1)), 0, 0, 209.000 + (lambda_perturbation * random.uniform(-1, 1)), 0, 0) # Clump LL
	#add_a_body(67627 + (a_perturbation * random.uniform(-1, 1)), 0, 0, 242.000 + (lambda_perturbation * random.uniform(-1, 1)), 0, 0) # Object 5 leading 
	#add_a_body(67627 + a_perturbation, 0, 0, 122.000, 0, 0) # Clump T
	#add_a_body(67627 - a_perturbation, 0, 0, 148.000, 0, 0) # Clump M
	#add_a_body(67627                 , 0, 0, 180.000, 0, 0) # Clump L
	#add_a_body(67627 + a_perturbation, 0, 0, 209.000, 0, 0) # Clump LL
	#add_a_body(67627 - a_perturbation, 0, 0, 242.000, 0, 0) # Object 5 leading 
	#add_a_body(67627 - (0.5 * a_perturbation), 0, 0, 122.000, 0, 0) # Clump T
	#add_a_body(67627                         , 0, 0, 148.000, 0, 0) # Clump M
	#add_a_body(67627 + (1.0 * a_perturbation), 0, 0, 180.000, 0, 0) # Clump L
	#add_a_body(67627                         , 0, 0, 209.000, 0, 0) # Clump LL
	#add_a_body(67627 - (0.5 * a_perturbation), 0, 0, 242.000, 0, 0) # Object 5 leading 
	#add_a_body(67627                         , 0, 0, 122.000, 0, 0) # Clump T
	#add_a_body(67627 - (1.0 * a_perturbation), 0, 0, 148.000, 0, 0) # Clump M
	#add_a_body(67627                         , 0, 0, 180.000, 0, 0) # Clump L
	#add_a_body(67627 + (1.0 * a_perturbation), 0, 0, 209.000, 0, 0) # Clump LL
	#add_a_body(67627                         , 0, 0, 242.000, 0, 0) # Object 5 leading 
	#add_a_body(67627                                    , 0, 0, 122.000, 0, 0) # Clump T
	#add_a_body(67627 + (np.sqrt(2) * a_perturbation / 2), 0, 0, 148.000, 0, 0) # Clump M
	#add_a_body(67627 - (1.0        * a_perturbation    ), 0, 0, 180.000, 0, 0) # Clump L
	#add_a_body(67627 + (np.sqrt(2) * a_perturbation / 2), 0, 0, 209.000, 0, 0) # Clump LL
	#add_a_body(67627                                    , 0, 0, 242.000, 0, 0) # Object 5 leading 
	add_a_body(67627 + (1.0 * a_perturbation), 0, 0, 122.000, 0, 0) # Clump T
	add_a_body(67627 - (1.0 * a_perturbation), 0, 0, 148.000, 0, 0) # Clump M
	add_a_body(67627 + (0.0 * a_perturbation), 0, 0, 180.000, 0, 0) # Clump L
	add_a_body(67627 + (1.0 * a_perturbation), 0, 0, 209.000, 0, 0) # Clump LL
	add_a_body(67627 - (1.0 * a_perturbation), 0, 0, 242.000, 0, 0) # Object 5 leading 
	#add_a_body(67627, 0, 0, 122.000 + (2.0 * lambda_perturbation), 0, 0) # Clump T
	#add_a_body(67627, 0, 0, 148.000 + (1.0 * lambda_perturbation), 0, 0) # Clump M
	#add_a_body(67627, 0, 0, 180.000 + (0.0 * lambda_perturbation), 0, 0) # Clump L
	#add_a_body(67627, 0, 0, 209.000 - (1.0 * lambda_perturbation), 0, 0) # Clump LL
	#add_a_body(67627, 0, 0, 242.000 - (2.0 * lambda_perturbation), 0, 0) # Object 5 leading 
	#add_a_body(67627, 0, 0, 180.000, 0, 0) # Clump L

def Nequals2(lambda_perturbation=0.0, a=2.308120E+06, mass=1.0E-17):
	add_a_body(a, 0, 0, 210.000 - (lambda_perturbation / 2.0), 0, 0, mass)
	add_a_body(a, 0, 0, 150.000 + (lambda_perturbation / 2.0), 0, 0, mass)

def Nequals3(lambda_perturbation=0.0, a=2.308120E+06, mass=1.0E-17, mode=0):
	if(mode == 0): # symmetric / linear
		add_a_body(a, 0, 0, 227.361 - (lambda_perturbation / 2.0), 0, 0, mass)
		add_a_body(a, 0, 0, 180.000, 0, 0, mass)
		add_a_body(a, 0, 0, 132.639 + (lambda_perturbation / 2.0), 0, 0, mass)
	elif(mode == 1): # antisymmetric / quadratic: I do not know if I need to multiply the lambda_perturbation by different coefficients for each body
		add_a_body(a, 0, 0, 227.361 - lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 180.000 + lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 132.639 - lambda_perturbation, 0, 0, mass)

def Nequals4(lambda_perturbation=0.0, a=2.308120E+06, mass=1.0E-17, mode=0):
	if(mode == 0): # linear, symmetric expansion
		add_a_body(a, 0, 0, 240.176 - (lambda_perturbation), 0, 0, mass)
		add_a_body(a, 0, 0, 198.678 - (lambda_perturbation / 2.0), 0, 0, mass)
		add_a_body(a, 0, 0, 161.322 + (lambda_perturbation / 2.0), 0, 0, mass)
		add_a_body(a, 0, 0, 119.824 + (lambda_perturbation), 0, 0, mass)
	if(mode == 1): # quadratic: I do not know if I need to multiply the lambda_perturbation by different coefficients for each body
		add_a_body(a, 0, 0, 240.176 + lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 198.678 - lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 161.322 - lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 119.824 + lambda_perturbation, 0, 0, mass)
	if(mode == 2): # cubic: I do not know if I need to multiply the lambda_perturbation by different coefficients for each body
		add_a_body(a, 0, 0, 240.176 - lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 198.678 + lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 161.322 - lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 119.824 + lambda_perturbation, 0, 0, mass)

def Nequals5(lambda_perturbation=0.0, a=2.308120E+06, mass=1.0E-17, mode=0):
	if(mode == 0): # linear, symmetric expansion
		add_a_body(a, 0, 0, 250.8615 - (lambda_perturbation), 0, 0, mass)
		add_a_body(a, 0, 0, 212.6600 - (lambda_perturbation / 2.0), 0, 0, mass)
		add_a_body(a, 0, 0, 180.0000, 0, 0, mass)
		add_a_body(a, 0, 0, 147.3400 + (lambda_perturbation / 2.0), 0, 0, mass)
		add_a_body(a, 0, 0, 109.1385 + (lambda_perturbation), 0, 0, mass)
	if(mode == 1): # quadratic: I do not know if I need to multiply the lambda_perturbation by different coefficients for each body
		add_a_body(a, 0, 0, 250.8615 + lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 212.6600 - lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 180.0000 - lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 147.3400 - lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 109.1385 + lambda_perturbation, 0, 0, mass)
	if(mode == 2): # cubic: I do not know if I need to multiply the lambda_perturbation by different coefficients for each body
		add_a_body(a, 0, 0, 250.8615 - lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 212.6600 + lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 180.0000, 0, 0, mass)
		add_a_body(a, 0, 0, 147.3400 - lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 109.1385 + lambda_perturbation, 0, 0, mass)
	if(mode == 3): # quartic: I do not know if I need to multiply the lambda_perturbation by different coefficients for each body
		add_a_body(a, 0, 0, 250.8615, 0, 0, mass)
		add_a_body(a, 0, 0, 212.6600 + lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 180.0000 - lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 147.3400 + lambda_perturbation, 0, 0, mass)
		add_a_body(a, 0, 0, 109.1385, 0, 0, mass)

#remove_all()
#Nequals2()
#Nequals3(-125, 1.0E-10)
#Nequals2(-115, 1.0E-13)
#Nequals3()
#Nequals4()
#Nequals5()
#add_body_randomly_in_ellipse()
# naive D68 simulations
#add_a_body(67627, 0, 0, 109.138, 0, 0)
#add_a_body(67627, 0, 0, 147.340, 0, 0)
#add_a_body(67627, 0, 0, 180.000, 0, 0)
#add_a_body(67627, 0, 0, 212.660, 0, 0)
#add_a_body(67627, 0, 0, 250.861, 0, 0)

# informed D68 simulations
#Obj5_trailing_D68_configuration()
#Obj5_leading_D68_configuration(a_perturbation=0.001)
#add_a_body(67627.0, 0, 0, 122.000, 0, 0) # Clump T
#add_a_body(67626.95, 0, 0, 148.000, 0, 0) # Clump M
#add_a_body(67627.0, 0, 0, 180.000, 0, 0) # Clump L
#add_a_body(67627.05, 0, 0, 209.000, 0, 0) # Clump LL
#add_a_body(67627.0, 0, 0, 242.000, 0, 0) # Object 5 leading 
#
#add_a_body()
#add_aeg_at_cer_contour(20)
#add_aeg_at_exact_cer()
#mu2 = bd.mu_Mim()
#mu3 = bd.mu_Aeg()
#remove_all()
#body2 = 'MIMAS'
#a2 = 185539 # in km
#body3 = 'AEGAEON'
#a3 = 167425 # in km # I think this value is off
#name_and_GM(body2, mu2) # I may have to scale mu2 to a different system
#flat_circular_orbit(a2)
#name_and_GM(body3, mu3) # I may have to scale mu2 to a different system
#flat_circular_orbit(a3)