# -*- coding: utf-8 -*- 


class Color():
	Red =   '\033[91m'
	Green = '\033[92m'
	Gray = '\033[01;30m'


	
def ColTex(Text, color = Color.Red):
	return '{green}{0}{endcolor}'.format( str(Text) , green=color, endcolor='\033[0m' )

def ColFloat(Text, color = Color.Red):
	return '{green}{:.8f}{endcolor}'.format( Text , green=color, endcolor='\033[0m' )