#!/usr/bin/env python
import sys
from html.parser import HTMLParser

class Includer(HTMLParser):
	"""Class that parses all SHTML files in input_dir, performs an include
	for each SSI (server-side include) comment, and writes results to output_dir as HTML files
	"""

	def __init__(self, input_dir, output_dir):
		super().__init__()
		self.input_dir = input_dir
		self.output_dir = output_dir

	def processFiles(self):
		"""Process all SHTML files in input_dir and write them as HTML files to output_dir"""
		print("input_dir: " + self.input_dir)
		print("output_dir: " + self.output_dir)
		

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: python3 html-include.py <input_dir> <output_dir>")
	else:
		includer = Includer(sys.argv[1], sys.argv[2])
		includer.processFiles()
