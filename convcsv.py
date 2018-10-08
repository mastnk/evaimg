#!/usr/bin/env python3
# -*- Coding: utf-8 -*-

import os
import sys

try:
	import cPickle as pickle
except:
	import pickle

if( len(sys.argv) < 2 ):
	print( 'Usage: {} file_title'.format(sys.argv[0]) )
	sys.exit()

pklfile = sys.argv[1] + '.pkl'
csvfile = sys.argv[1] + '.csv'

try:
	with open(pklfile, 'rb') as fp:
		data = pickle.load( fp )
except:
	data = {}

csv_data = []
for key, value in data.items():
	csv_data.append( '{key},{value}'.format(key=key, value=value) )
csv_data.sort()


with open( csvfile, 'w' ) as fp:
	for line in csv_data:
		print( line )
		fp.write( line+'\n' )

