#!/usr/bin/env python3
# -*- Coding: utf-8 -*-

HTML='''
<html>
<header>
<title> Evaluate Image </title>
<link rel="shortcut icon" href="favicon.ico" >
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</header>
<body bgcolor="#AAAAAA" oncontextmenu="return false;">


<center>
{body}
</center>

</body>
</html>
'''

import cgitb; cgitb.enable()
import cgi

import os
import sys
import glob
import random
import fcntl
import re
try:
	import cPickle as pickle
except:
	import pickle


EXT = 'png'
PREFIX =  'EVA_'

def output( body = '' ):
	print('Content-type: text/html')
	print
	print( HTML.format(body=body) )
	sys.exit()

def output_thanks():
	body = '''
<table border="0">
<tr>
<td align="center" valign="middle"><img src="Bee.png"></td>
<td><font size="10"><b>
Thanks!
</b></font></td>
</tr>
</table>
'''
	output( body )

def output_error( msg = '' ):
	body = '<font color="red" size="7">!! ERROR !!</font><br />'
	body += msg
	output( body )

def load_lst( filename ):
	dirlist = []
	with open( filename, 'r' ) as fp:
		for line in fp:
			dirlist.append( line.strip() )
	return dirlist

def analyze( lst, cur, id, form ):
	fd = open('{lst}.lock'.format(lst=lst), 'w')
	fcntl.flock(fd,fcntl.LOCK_EX)
	
	pklfile = '{lst}.pkl'.format(lst=lst)
	try:
		with open(pklfile, 'rb') as fp:
			data = pickle.load( fp )
	except:
		data = {}
	
	for key in form.keys():
		if( key.startswith( PREFIX ) ):
			k = key[len(PREFIX):]
			k = '{id},{cur},{name}'.format(id=id, cur=cur, name=k)
			data[k] = int(form[key].value)
	
	with open(pklfile, 'wb') as fp:
		pickle.dump( data, fp )
	
	fcntl.flock(fd,fcntl.LOCK_UN)
	fd.close()
	

form = cgi.FieldStorage()

if( 'lst' in form ):
    lst = form['lst'].value
else:
	output_error( 'not found "lst" in form' )

if( 'id' in form ):
    id = form['id'].value
else:
	output_error( 'not found "id" in form' )

try:
	dirlist = load_lst( lst+'.lst' )
except:
	output_error( 'file not found: {}'.format(lst) )

if( 'ind' in form ):
	try:
		ind = int( form['ind'].value )
	except:
		output_error( 'ind: {}'.format(form['ind'].value) )
else:
	ind = 0

if( ind < 0 or ind > len(dirlist) ):
	output_error( 'out of range ind: {}'.format(ind) )

if( ind > 0 ):
	analyze( lst, dirlist[ind-1], id, form )

if( ind ==  len(dirlist) ):
	output_thanks()

cur = dirlist[ind]

imgfile = '{}/*.{}'.format( cur, EXT )
try:
	imglist = glob.glob( imgfile )
except:
	output_error( 'file not found: {}'.format(imgfile) )

random.shuffle(imglist)

body = ''

##############################################################
head ='''
<table border="0">
<tr>
<td align="center" valign="middle"><img src="Bee.png"></td>
<td><font size="5"><b>
ID: {id} <br />
{cur} in {lst} ({ind}/{length})
</b></font></td>
</tr>
</table>
<hr />
'''.format(id=id, cur=cur, lst=lst, ind=ind+1, length=len(dirlist))

body += head


##############################################################
body += '''
<form method="post" action="evaimg.cgi?id={id}&lst={lst}&ind={ind}">
'''.format(id=id, lst=lst, ind=ind+1)

templ = '''
<img src="{src}" border="0"><br />
BAD &larr;
<font size="+2">
1<input type="radio" name="{pre}{name}" value="1"> &nbsp;&nbsp;
2<input type="radio" name="{pre}{name}" value="2"> &nbsp;&nbsp;
3<input type="radio" name="{pre}{name}" value="3"> &nbsp;&nbsp;
4<input type="radio" name="{pre}{name}" value="4"> &nbsp;&nbsp;
5<input type="radio" name="{pre}{name}" value="5" required> 
</font>
&rarr;GOOD
<br /><br /><hr />
'''

for filename in imglist:
	s = re.search( r'/.*?\.{}'.format(EXT), filename )
	name = s.group()
	name = name[1:-1-len(EXT)]
	body += templ.format(src=filename, name=name, pre=PREFIX)

body += '''
<input type="submit" value="SUBMIT">
</form>
'''

##############################################################
output( body )
