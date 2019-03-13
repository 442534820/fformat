#!/usr/bin/python
imoirt os
import sys

self_name = ""

HELP_STR = "{--2unix | --2dos | --view | --rightsXXX | --help}[--filter {.c.h.S}]"
f_filter = set(('.S', '.c', '.h'))

def is_dos_file(file_name):
	cmd = 'file' + file_name
	rl = os.popen(cmd)
	info = rl.readlines()
	for line in info:
		if line.find("with CRLF line terminators") > 0:
			return True
	return False

def dos2unix_process(cwd):
	curr_dir = os.listdir(cwd)
	for file in curr_dir:
		path = os.path.join(cwd, file)
		if file.startswith('.'):
			continue
		if os.path.isdir(path):
			dos2unix_process(path)
		else:
			if len(f_filter) > 0:
				if os.path.splitext(path)[1] not in f_filter:
					continue
				if is_dos_file(path):
					print file + " is a dos file, convert to unix..."
					os.popen('dos2unix ' + path)
				else:
					print file + " is unix file, skip..."

def unix2dos_process(cwd):
	curr_dir = os.listdir(cwd)
	for file in curr_dir:
		path = os.path.join(cwd, file)
		if file.startswith('.'):
			continue
		if os.path.isdir(path):
			unix2dos_process(path)
		else:
			if len(f_filter) > 0:
				if os.path.splitext(path)[1] not in f_filter:
					continue
				if is_dos_file(path):
					print file + " is dos file, skip..."
				else:
					print file + " is a unix file, convert to dos..."
					os.popen("unix2dos " + path)

def rights_process(cwd, right):
	curr_dir = os.listdir(cwd)
	for file in curr_dir:
		path = os.path.join(cwd, file)
		if file.startswith('.'):
			continue
		if os.path.isdir(path):
			rights_process(path, right)
		else:
			if len(f_filter) > 0:
				if os.path.splitext(path)[1] not in f_filter:
					continue
			print "formating: " + path + " to " + right
			os.system("chmod " + right + " " + path)

def view_all_file_type(cwd):
	curr_dir = os.listdir(cwd)
	for file in curr_dir:
		path = os.path.join(cwd, file)
		if os.path.isdir(path):
			view_all_file_type(path)
		else:
			os.system("file " + path)

def filter_parser(filter_str):
	print "filter: " + filter_set
	fl = filter_str.split('.')
	fl = filter(None, fl)
	f_filter.clear()
	for f in fl:
		f_filter.add("." + f)


if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print "usage: " + sys.argv[0] + " " + HELP_STR
		sys.exit()
	
	self_name = __file__
	cur_path = os.getcwd()
	if len(sys.argv) == 4:
		if sys.argv[2] == "--filter":
			filter_parser(sys.argv[3])
	if sys.argv[1] == "--2unix":
		dos2unix_process(cur_path)
	elif sys.argv[1] == "--2dos":
		unix2dos_process(cur_path)
	elif sys.argv[1] == "--view":
		view_all_file_type(cur_path)
	elif "--rights" in sys.argv[1]:
		print "rights format"
		rights_process(cur_path, sys.argv[1].replace("--rights", ""))
	elif sys.argv[1] == "--help":
		print "usage: " + sys.argv[0] + " " + HELP_STR
		sys.exit()
	else:
		print "usage: " + sys.argv[0] + " " + HELP_STR
		sys.exit()
