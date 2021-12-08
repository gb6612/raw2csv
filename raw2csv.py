#!python

# raw2csv
# Translates SPICE3 raw data into CSV file format.
# Used, for example, in conjunction with ngSpice simulator output data.
# 
# > raw2csv.py [-o <output_file.csv>] [-t] <input_raw_file>
# 
# -o : output csv file. Default is "out.csv" in the current directory
# -t : transpose output. By default data is aligned in column
# <input_raw_file>: mandatory input file
#
# Under MIT License (MIT)
# Copyright (C) 2021 Gabriele Bellini <Switzerland>


import argparse
import sys
import os
import time

parser = argparse.ArgumentParser(description='Translate SPICE3 raw data into CSV file format')
parser.add_argument('-t', 
                    action='store_true',
                    dest='t',
                    help='transpose data'
                    )

parser.add_argument('-o', 
                    default='out.csv',
                    dest='outfile',
                    help='output CSV filename (default is out.csv)',
                    type=str 
                    )

parser.add_argument('inputfile', 
                    help='input raw file (mandatory)',
                    type=str 
                    )

args=parser.parse_args()
transpose=args.t

starttime = time.time()

print('Input file  : ' + args.inputfile)
print('Output file : ' + args.outfile)

result = []
result_line = []
line_splitted = []
f = open(args.inputfile, 'r')

while True:
    currline = f.readline()
    if ("" == currline):
        break
    if (currline.find('No. Variables:') >= 0):  # search for nb of variables
        line_splitted = currline.split(':')
        nb_variables = line_splitted[1].rstrip('\n')
        print('found '+nb_variables+' variables')
        break
    
while True:
    currline = f.readline()
    if ("" == currline):
        break
    if (currline.find('Variables:') >= 0):  
        #print('Variables')
        break

for i in range(int(nb_variables)):
    currline = f.readline()
    if ("" == currline):
        break
    currline = currline.strip('\t')
    currline = currline.rstrip('\n')
    result_line = (currline.split('\t'))
    result.append(result_line)

while True:
    currline = f.readline()
    if ("" == currline):
        break
    if (currline.find('Values:') >= 0):  
        print('Processing values')
        break

endoffile=0
while True:
    for i in range(int(nb_variables)):
        currline = f.readline()
        if ("" == currline):
            endoffile=1
            break
        if len(currline.strip())>0:  # ignore empty lines
            #print(currline)
            line_splitted = currline.split('\t')   
            result[i].append(line_splitted[-1].rstrip('\n')) # take last/actual value and cleanup newline
    if (endoffile>0):
        break

f.close()

new_result=[]
##############################
# Transpose ?
if (transpose):
    new_result = [[result[j][i] for j in range(len(result))] for i in range(len(result[0]))]
else:
    new_result = result

##############################
# Write result to file
f = open(args.outfile, 'w')

for n in new_result:
    s=",".join(n)
    s=s+"\n"
    #print(s)
    f.write(s)

f.close()
 
#for n in new_result:
#    print(n)

endtime = time.time()
print('Execution time in seconds: ', (endtime-starttime))

    