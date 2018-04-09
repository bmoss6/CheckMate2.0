#!/usr/bin/env python3
import configparser

## Config object to read in configuration file 
class Conf(object):
	
	## Constructor
	def __init__(self):
		super(Conf, self).__init__()
		self.config = configparser.ConfigParser()
		self.config.read('config.ini')
	
	## Get Interger type
	# @param obj:string main section
	# @param var:string variable
	# @return type:int interger representation of object 
	def I(self,obj,var):
		return int(self.config[obj][var])

	## Get String type
	# @param obj:string main section
	# @param var:string variable
	# @return type:string interger representation of object 
	def S(self,obj,var):
		return self.config[obj][var]
