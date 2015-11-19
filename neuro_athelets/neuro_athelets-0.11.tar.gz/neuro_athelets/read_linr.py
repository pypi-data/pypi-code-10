'''
This file is used for linear regression, which after using weka has been proved to have nothing relevant. 
Therefore not used. However the functions here can be used for others reading in csv files and return matrix, as explained by the functional documentations. 
'''

import numpy as np
import scipy as sp
def is_number(s):
	'''
	Args:
		s: the String input. 
	Returns:
		Boolean: True if is number, False otherwise. 
	'''
	try:
		float(s)
		return True
	except:
		return False

def csv2matrix(name,burn_line = 1):
	'''
	This function reads in the name specified csv and outputs a matrix. 
	The optional arguments is to specify if the first line can be ignored or not. 
	Assumes that the file is a matrix other than unformmated data. 
    Args:
		name: string of filename
		burn_line: int of how many lines to burn at front. Defaults to 1. 
	Returns:
		numpy float array of matrix. 	
	'''
	number_index = -1
	result = []
	with open(name, 'r') as f:
		for line in f:
			if burn_line !=0:
				burn_line-=1
				continue
			
			#get to the split where its a number, record it. 
		   	line_split = line.split(',')
			if number_index == -1:
				for i in range(len(line_split)):
					if is_number(line_split[i]):
						number_index = i
						break
			
			#if number_index is set
			result.append([float(item) for item in line_split[number_index:]])	
	try:
		result = np.array(result).astype(float)
		return result
	except e:
		print 'ERROR in csv2matrix while converting to np float array:'
		print e	
		

def main():
	print 'this is main'
	
if __name__ == '__main__':
	data = csv2matrix('athlete_data.csv')
