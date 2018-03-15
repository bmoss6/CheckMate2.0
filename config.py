#!/usr/bin/env python3
import configparser


class Conf(object):
	"""docstring for conf"""
	def __init__(self):
		super(Conf, self).__init__()
		self.config = configparser.ConfigParser()
		self.config.read('config.ini')
	
	#Get Interger
	def I(self,obj,var):
		return int(self.config[obj][var])

	#Get String
	def S(self,obj,var):
		return self.config[obj][var]
