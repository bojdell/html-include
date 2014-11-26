#!/usr/bin/env python
import sys
import re
from os import listdir
from os import path
from bs4 import BeautifulSoup
from bs4 import Comment

class Includer():
	"""Class that parses all SHTML files in input_dir, performs an include
	for each SSI (server-side include) comment, and writes results to output_dir as HTML files
	"""

	def __init__(self, input_dir, output_dir):
		super().__init__()
		self.input_dir = input_dir
		self.output_dir = output_dir
		self.shtml_files = []
		self.inc_files = []

		# set default indent to 4 spaces in BeautifulSoup.prettify()
		orig_prettify = BeautifulSoup.prettify
		r = re.compile(r'^(\s*)', re.MULTILINE)
		def prettify(self, encoding=None, formatter="minimal", indent_width=4):
		    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
		BeautifulSoup.prettify = prettify

	def processFiles(self):
		"""Process all SHTML files in input_dir and write them as HTML files to output_dir"""

		# iterate over all files in self.input_dir, collecting all .shtml and .inc files
		for f in listdir(self.input_dir):
			fName, fExt = path.splitext(f)
			if fExt == ".shtml":
				self.shtml_files.append(f)
			elif fExt == ".inc":
				self.inc_files.append(f)

		# process each .shtml file individually via self.__processFile()
		for f in self.shtml_files:
			fName = path.splitext(f)[0]
			input_file = self.input_dir + '/' + f
			output_file = self.output_dir + '/' + fName + ".html"
			self.__processFile(input_file, output_file, False)

	def __processFile(self, input_file, output_file, recursing):
		"""Process a single file at path input_file and write processed file to path output_file.
		May be called recursively depending on template structure.
		"""
		f_in = open(input_file, "r", encoding="utf-8")
		soup = BeautifulSoup(f_in)

		# find all comments in the document
		comments = soup.findAll(text=lambda text:isinstance(text, Comment))

		# parse out the template filepath from each comment, recursively obtain the content,
		# and replace the comment with the content to be inserted
		for comment in comments:
			# TODO: fix regex to include 'file' keyword
			inc_path = re.match('^#include.+?virtual=\"(.+?)\"', comment).group(1)
			if inc_path:
				inc_content = BeautifulSoup(self.__processFile(self.input_dir + '/' + inc_path, "", True))
				for tag in inc_content.findAll(True):
					comment.insert_before(tag)
				comment.extract()
		f_in.close()

		# if we are recursing, return our result as a string so it can be included recursively
		if recursing:
			return soup.prettify(formatter=None)

		# if not, this must be the original SHTML file, so write our result to output_file as an HTML document
		else:
			f_out = open(output_file, "w", encoding="utf-8")
			f_out.write(soup.prettify(formatter=None))
			f_out.close()

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: python3 html-include.py <input_dir> <output_dir>")
	else:
		includer = Includer(sys.argv[1], sys.argv[2])
		print("Processing files in: " + sys.argv[1])
		includer.processFiles()
		print("Files processed successfully. Written to: " + sys.argv[2])

