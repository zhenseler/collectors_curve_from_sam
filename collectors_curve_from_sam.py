'''
Create a Collector's curve from a folder filled with .sam files

Dependencies:

	- numpy

Usage:

	- python collectors_curve_from_sam.py <input_folder_path> <number_of_reps_to_run>
		<output_file>


'''

from sys import argv
import numpy
from os import listdir



input_folder = argv[1]
number_of_samplings = int(argv[2])
output_name = argv[3]

out = open(output_name, 'w')
ID_length_max = 0
output_list = []
sample_list = []

for filename in listdir(input_folder):
	if filename.endswith('.sam'):
		print('Currently running on ' + filename)
		sample_name = filename.split('_')[0]
		sample_list.append(sample_name)
		ID_list = []
		iteration_list = []
		for l in open(input_folder + filename,'U'):
			if l.startswith('@') == False:
				ID_list.append(l.split('\t')[2])
		ID_list_length = len(ID_list)
		if ID_list_length == 0:
			continue
		if ID_list_length > ID_length_max:
			ID_length_max = ID_list_length
		for subset_iteration in range(number_of_samplings):
			subset_result_list = []
			for subset_depth in range(ID_list_length + 1):
				ID_list_subset = list(numpy.random.choice(ID_list, subset_depth, False))
				subset_result_list.append(len(set(ID_list_subset)))
			iteration_list.append(subset_result_list)
		array = numpy.array(iteration_list)
		output_list.append(list(numpy.average(array, axis = 0)))

out.write('Subset_depth\t'+'\t'.join(sample_list)+'\n')
for n in range(ID_length_max):
	write_list = [str(n)]
	for sample in output_list:
		try:
			write_list.append(str(sample[n]))
		except IndexError:
			write_list.append('')
	out.write('\t'.join(write_list)+'\n')

out.close()