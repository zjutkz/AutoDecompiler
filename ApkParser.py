#!/usr/bin/env python
#-*-coding:utf-8-*- 

import sys
import subprocess
import threading
import os
import re

class Parser(object):
	def __init__(self,apk_path):
		self.apk_path = apk_path
		self.apk_name = self.parseName(self.apk_path)
		self.parent_path = os.path.dirname(apk_path)
		self.decompile_file_path = self.parent_path + "/" + self.apk_name
		self.process = None
	
	def parseName(self,apk_path):
		splittable = apk_path.split('/')
		full_apk_name = splittable[len(splittable) - 1]
		return full_apk_name.split('.')[0]

	def decompile(self):
		print '.....decompile started.....'
		def doDecompile():
			apktool_cmd = "apktool d " + self.apk_path
			self.process = subprocess.Popen(apktool_cmd, shell=True)
			self.process.communicate()

		thread = threading.Thread(target=doDecompile)
		thread.start()
		thread.join()
		print '.....decompile finished.....'

	def recompile(self):
		print '.....recompile started.....'
		def doRecompile():
			apktool_cmd = "apktool b " + self.decompile_file_path
			self.process = subprocess.Popen(apktool_cmd, shell=True)
			self.process.communicate()

		thread = threading.Thread(target=doRecompile)
		thread.start()
		thread.join()
		print '.....recompile finished.....'

	def dex_to_jar(self):
		print '.....dex2jar started.....'
		dest = self.decompile_file_path + "/build/apk/"
		for filename in os.listdir(dest):
			if not filename.find("classes"): 
				def doDex_to_jar():
					cmd = "./d2j-dex2jar.sh " + self.decompile_file_path + "/build/apk/" + filename
					self.process = subprocess.Popen(cmd, shell=True)
					self.process.communicate()

				thread = threading.Thread(target=doDex_to_jar)
				thread.start()
				thread.join()
		print '.....dex2jar finished.....'

	def run(self):
		self.decompile()
		self.recompile()
		self.dex_to_jar()

def parse():
	parser = Parser(sys.argv[1])
	parser.run()

if __name__ == "__main__":
    parse()


