#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands
import uuid

"""Copy Special exercise
The copyspecial.py program takes one or more directories as its arguments. 
We'll say that a "special" file is one where the name contains the pattern 
__w__ somewhere, where the w is one or more word chars. The provided main() 
includes code to parse the command line arguments, but the rest is up to you. 
Write functions to implement the features below and modify main() to call 
your functions.

Suggested functions for your solution(details below):

get_special_paths(dir) -- returns a list of the absolute paths of the special 
files in the given directory 
copy_to(paths, dir) given a list of paths, copies 
those files into the given directory 

zip_to(paths, zippath) given a list of paths, 
zip those files up into the given zipfile

"""

# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(dir):
  fullPath = os.path.abspath(dir)
  files = os.listdir(fullPath)
  fileList = []
  for filename in files:
    if None != re.search('__\w+__', filename) :
      fileList.append(os.path.join(fullPath,filename))
  return fileList
  
def copy_to(paths, dir):
  if not os.path.exists(dir):
    # if we don't do this the copy util could create a file with the same name as dir
    raise Exception('Destination directory does not exist: \"' + dir + '\"')
  for filename in paths:
    shutil.copy(filename, dir) 
  return

def zip_to(paths, zippath):
  currdir= os.getcwd()
  tempdir = os.path.abspath('.\\' + uuid.uuid4().hex)
  try:
    os.mkdir(tempdir)
    os.chdir(tempdir)
    copy_to(paths, tempdir)
    shutil.make_archive(zippath, 'zip', base_dir='.')
  finally:
    os.chdir(currdir)
    shutil.rmtree(tempdir)
  return
  


def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if len(args) > 0 and args[0] == '--todir':
    todir = os.path.abspath(args[1])
    del args[0:2]

  tozip = ''
  if len(args) > 0  and args[0] == '--tozip':
    tozip = os.path.abspath(args[1])
    del args[0:2]

  if len(args) <= 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  #for now we're just piping the function through for testing purposes. 
  paths= []
  for directory in args:
    paths += get_special_paths(directory)
  
  if '' != todir:
    copy_to(paths, todir)
  if '' != tozip: 
    zip_to(paths,tozip) 
  return
 
if __name__ == "__main__":
  main()
