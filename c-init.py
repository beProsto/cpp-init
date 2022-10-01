#!/usr/bin/env python3

# ###
# I've grown irritated with having to set up the project structure 
# for every single one of my c/cpp projects xd
# so I decided to make a simple python script to handle that for me lol
# ###

import sys
import os

# Recursively creates directories
def makeDirectory(name):
	naems = name.split("/");
	if naems[0] == ".":
		makeDirectory(name[2 : len(name)])
		return
	try:
		os.mkdir("./" + naems[0])
	except:
		pass
	name = name[len(naems[0])+1 : len(name)]
	if len(name) > 0:
		os.chdir(naems[0])
		makeDirectory(name)
		os.chdir("..")

# Recursively creates a file with custom contents in it
def makeFile(name, contents=""):
	naems = name.split("/");
	if len(naems) > 1:
		makeDirectory(name[0 : -len(naems[-1])])
	fp = open(name, 'w')
	fp.write(contents)
	fp.close()

# Opens and dumps a file into a string
def loadFile(name):
	fp = open(os.path.dirname(os.path.abspath(__file__)) + "/c-init-res/" + name, "r")
	data = fp.read()
	fp.close()
	return data

# Project setup data
class ProjectSetup:
	isProjectCpp = False
	isProjectLibrary = False
	isProjectCmake = False
	detectedArgs = False

def scanArg(arg):
	ProjectSetup.isProjectCpp = not (arg[0] == 'c')
	ProjectSetup.isProjectLibrary = not (arg[1] == 'a')
	ProjectSetup.isProjectCmake = not (arg[2] == 'm')
	ProjectSetup.detectedArgs = True

# Application's entry point
def main():
	# Scan arguments for options
	arguments = sys.argv[1:]
	for arg in arguments:
		if len(arg) == 3:
			scanArg(arg)
			break

	# If we didn't detect options, spit out a warning
	if not ProjectSetup.detectedArgs:
		print("Didn't detect any options.")
		print("Automatically setting to 'cam':")
		print("- c - C (use x for C++)")
		print("- a - Application (use l for Library)")
		print("- m - Build with make (use c for Cmake)")
		accept = input("Do you accept these options? <y/n>:")
		if accept != 'y' and accept != 'Y':
			return
		else:
			print("Continuing with 'cam'...")
	
	# We now have ProjectSetup data
	sourcepath = "main.c"
	includepath = "main.h"
	if ProjectSetup.isProjectLibrary:
		sourcepath = "lib.c"
		includepath = "lib.h"
	if ProjectSetup.isProjectCpp:
		sourcepath += "pp"
		includepath += "pp"
	
	# Makefile setup
	if not ProjectSetup.isProjectCmake:
		makefile = loadFile("Makefile")
		compiler = "$(CC)"
		name = "app"
		winext = ".exe"
		linext = ""
		cloptions = ""
		if ProjectSetup.isProjectLibrary:
			name = "libmylib"
			winext = ".dll"
			linext = ".so"
			cloptions = "-DLIB_BUILD_SHARED -shared"
		if ProjectSetup.isProjectCpp: 
			compiler = "$(CXX)"
		makefile = makefile.replace(r"{sourcepath}", sourcepath)
		makefile = makefile.replace(r"{compiler}", compiler)
		makefile = makefile.replace(r"{name}", name)
		makefile = makefile.replace(r"{winext}", winext)
		makefile = makefile.replace(r"{linext}", linext)
		makefile = makefile.replace(r"{cloptions}", cloptions)
		makeFile("Makefile", makefile)

	# File contents
	gitignore = loadFile("_gitignore")
	source = loadFile(sourcepath)
	include = loadFile(includepath)

	# File structure creation
	makeFile("build/.build")
	makeFile(".gitignore", gitignore)
	makeFile("src/" + sourcepath, source)
	makeFile("include/" + includepath, include)


if __name__ == "__main__":
	main()