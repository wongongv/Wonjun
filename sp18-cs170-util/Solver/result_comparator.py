import os
import pdb
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from student_utils_sp18 import *
from networkx.algorithms import approximation
import unionfind
import itertools
import networkx.algorithms as algo

def compare_by_file(input_file, compare1, compare2, output_directory, params=[]):
	print('Processing', input_file)

	global fromcomp1
	global fromcomp2

	global totalcost1 
	global totalcost2 
	global totalcostcombined 
	global equallygood

	input_data = utils.read_file(input_file)
	compare_data1 = utils.read_file(compare1)
	compare_data2 = utils.read_file(compare2)

	number_of_kingdoms, list_of_kingdom_names, starting_kingdom, adjacency_matrix = data_parser(input_data)

	G = adjacency_matrix_to_graph(adjacency_matrix)
	comp1_kingdom_tour_name = compare_data1[0]
	comp1_conquered_kingdoms_name = compare_data1[1]

	comp2_kingdom_tour_name = compare_data2[0]
	comp2_conquered_kingdoms_name = compare_data2[1]

	comp1_kingdom_tour_index = convert_kingdom_names_to_indices(comp1_kingdom_tour_name, list_of_kingdom_names)
	comp1_conquered_kingdoms_index = convert_kingdom_names_to_indices(comp1_conquered_kingdoms_name, list_of_kingdom_names)


	comp2_kingdom_tour_index = convert_kingdom_names_to_indices(comp2_kingdom_tour_name, list_of_kingdom_names)
	comp2_conquered_kingdoms_index = convert_kingdom_names_to_indices(comp2_conquered_kingdoms_name, list_of_kingdom_names)


	cost1 = cost_of_solution(G, comp1_kingdom_tour_index, comp1_conquered_kingdoms_index)[0]
	cost2 = cost_of_solution(G, comp2_kingdom_tour_index, comp2_conquered_kingdoms_index)[0]

	
	if cost1 == 'infinite':
		print(compare1)
		raise Exception("not a valid outputs!!!")
	elif cost2 =='infinite':
		print(compare2)
		raise Exception("not a valid outputs!!!")

	basename, filename = os.path.split(input_file)
	output_filename = utils.input_to_output(filename)
	output_file = '{}/{}'.format(output_directory, output_filename)
	
	if not os.path.exists(output_directory):
		os.makedirs(output_directory)

	totalcost1 += cost1
	totalcost2 += cost2
	if cost1 < cost2:
		totalcostcombined += cost1
		fromcomp1 += 1
		utils.write_data_to_file(output_file, comp1_kingdom_tour_name, ' ')
		utils.write_to_file(output_file, '\n', append=True)
		utils.write_data_to_file(output_file, comp1_conquered_kingdoms_name, ' ', append=True)
	else :	
		if cost1 == cost2 :
			equallygood +=1
		else:
			fromcomp2 += 1
		totalcostcombined += cost2
		utils.write_data_to_file(output_file, comp2_kingdom_tour_name, ' ')
		utils.write_to_file(output_file, '\n', append=True)
		utils.write_data_to_file(output_file, comp2_conquered_kingdoms_name, ' ', append=True)


def compare_all(input_directory, comp1dir, comp2dir, output_directory, params=[]):
	input_files = utils.get_files_with_extension(input_directory, 'in')
	comp1_files = utils.get_files_with_extension(comp1dir, 'out')
	comp2_files = utils.get_files_with_extension(comp2dir, 'out')

	inputdirleng = len(input_directory)
	il =list(input_files)
	ill = [i[inputdirleng + 1:-3] for i in il]

	comp1dirleng = len(comp1dir)
	c1 =list(comp1_files)
	c1l =[i[comp1dirleng + 1:-4] for i in c1]
	
	comp2dirleng = len(comp2dir)
	c2 =list(comp2_files)
	c2l =[i[comp2dirleng + 1:-4] for i in c2]

	for i in c1l:
		if i in ill and i in c2l:
			compare_by_file(input_directory+"/"+i+'.in',comp1dir+"/"+i+'.out' ,comp2dir+"/"+i+'.out', output_directory,params=params)

	# global count
	# global localcount
	# print("count : ", count)
	# print("localcount : ", localcount)

if __name__=="__main__":


	fromcomp1 = 0
	fromcomp2 = 0
	totalcost1 = 0
	totalcost2 = 0
	equallygood = 0
	totalcostcombined = 0
	parser = argparse.ArgumentParser(description='Parsing arguments')
	parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
	parser.add_argument('input', type=str, help='The path to the input file or directory')
	parser.add_argument('compare1', type=str, help='The path to the input file or directory')
	parser.add_argument('compare2', type=str, help='The path to the input file or directory')
	parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
	parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
	args = parser.parse_args()

	output_directory = args.output_directory

	if args.all:
		input_directory = args.input
		comp1_directory = args.compare1
		comp2_directory = args.compare2
		compare_all(input_directory, comp1_directory, comp2_directory, output_directory, params=args.params)
	else:
		input_file = args.input
		compare_file1 = args.compare1
		compare_file2 = args.compare2
		compare_by_file(input_file, compare_file1, compare_file2, output_directory, params=args.params)

	print("fromcomp1 :", fromcomp1)
	print("fromcomp2 :", fromcomp2)
	print("equallygood :", equallygood)
	print("total cost of comp1 :", totalcost1)
	print("total cost of comp2 :", totalcost2)
	print("total cost of combined :", totalcostcombined)
	print("better is better by :", abs(totalcost1 - totalcost2))
	print("Gain :", abs(min(totalcost1, totalcost2) - totalcostcombined))