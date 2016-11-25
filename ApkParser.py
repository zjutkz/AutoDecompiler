#!/usr/bin/env python
#-*-coding:utf-8-*- 

import sys
import subprocess
import threading
import os
import shutil 

class Parser(object):
	def __init__(self,path):
		self.current_path = self.current_path()
		self.output = self.current_path + "/output"
		self.apk_path = path[1]
		self.dex_to_jar_path = self.get_dex_to_jar_path()
		self.apk_name = self.parseName(self.apk_path)
		self.parent_path = os.path.dirname(self.apk_path)
		self.process = None
	
	def get_dex_to_jar_path(self):
		with open(self.current_path + "/Config.py") as f:
			return f.readlines()[3].split("=")[1].strip()

	def current_path(self):
		return os.path.normpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))

	def parseName(self,apk_path):
		splittable = apk_path.split('/')
		full_apk_name = splittable[len(splittable) - 1]
		return full_apk_name.split('.')[0]

	def copyApk(self):
		shutil.move(self.apk_path, self.dex_to_jar_path)   

	def changeEnv(self):
		os.chdir(self.dex_to_jar_path)

	def decompile(self):
		print '.....decompile started.....'
		def doDecompile():
			apktool_cmd = "apktool d " + self.apk_name + ".apk"
			self.process = subprocess.Popen(apktool_cmd, shell=True)
			self.process.communicate()

		thread = threading.Thread(target=doDecompile)
		thread.start()
		thread.join()
		print '.....decompile finished.....'

	def recompile(self):
		print '.....recompile started.....'
		def doRecompile():
			apktool_cmd = "apktool b " + self.apk_name
			self.process = subprocess.Popen(apktool_cmd, shell=True)
			self.process.communicate()

		thread = threading.Thread(target=doRecompile)
		thread.start()
		thread.join()
		print '.....recompile finished.....'

	def dex_to_jar(self):
		print '.....dex2jar started.....'
		dest = self.apk_name + "/build/apk/"
		for filename in os.listdir(dest):
			if not filename.find("classes"): 
				def doDex_to_jar():
					cmd = "./d2j-dex2jar.sh " + self.apk_name + "/build/apk/" + filename
					self.process = subprocess.Popen(cmd, shell=True)
					self.process.communicate()

				thread = threading.Thread(target=doDex_to_jar)
				thread.start()
				thread.join()
		print '.....dex2jar finished.....'

	def createDir(self):
		os.mkdir(self.output)

	def restoreFile(self):
		shutil.move(self.apk_name, self.output)    
		for dex in os.listdir(self.dex_to_jar_path):
			if not dex.find("classes"): 
				shutil.move(dex, self.output)    

	def run(self):
		self.copyApk()
		self.changeEnv()
		self.decompile()
		self.recompile()
		self.dex_to_jar()
		self.createDir()
		self.restoreFile()

def parse():
	parser = Parser(sys.argv)
	parser.run()

if __name__ == "__main__":
    parse()


