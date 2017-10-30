# -*- coding: utf-8 -*-
import collections

class Resource:
	''' resource class
	store value in data[major][value.name]
	'''
	def __init__(self,objs=None):
		self.data = collections.OrderedDict()
		if objs is not None:
			for a_obj in objs:
				self.addObj(a_obj)

	def add_with_key(self, major_key, minor_key, value):
		if not major_key in self.data.keys():
			self.data[major_key] = collections.OrderedDict()
		self.data[major_key][minor_key] = value

	def addObj(self, obj):
		'''
		use the __class__.__name__ of obj as the major key (string type)
		use the name of obj as the minor key
		data[obj.__class__.__name__][obj.name] = obj
		'''
		if not obj.__class__.__name__ in self.data.keys():
			self.data[obj.__class__.__name__] = collections.OrderedDict()
		self.data[obj.__class__.__name__][obj.name] = obj

	def check_minor_keys(self, a_major_key, minor_key_list):
		a_list = list(self.data[a_major_key].keys())
		for a_name in minor_key_list:
			if a_name not in a_list:
				sys.exit('The key {0} may not be registered. ".\nRegistered list are the followings:\n{1}'.format(a_name,'\n'.join(a_list)))

	def __getitem__ (self, major_key):
		return self.data[major_key]
