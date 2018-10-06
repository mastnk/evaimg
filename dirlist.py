#!/usr/bin/env python3
# -*- Coding: utf-8 -*-

class dirlist:
	def load( self, filename ):
		with open( filename, 'r' ) as fp:
			self.dirlist = []
			for line in fp:
				self.dirlist.append( line.strip() )
	
	def first( self ):
		return self.dirlist[0]

	def next( self, cur ):
		idx = self.dirlist.index( cur )
		idx += 1
		if( idx >= len(self.dirlist) ):
			return ''
		return self.dirlist[idx]

if( __name__ == '__main__' ):
	dl = dirlist()
	dl.load( 'sample' )
	print( dl.dirlist )
	
	next = 'girl'
	while( next != None ):
		next = dl.next( next )
		print( next )
