#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
def second_word(s): 
  match = re.search(r'-\w+-(?P<desired_word>\w+).jpg', s)
  if not match: 
    return s
  else: 
    return match.group('desired_word')

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  #extract the filename
  match =  re.search(r'\S+_(?P<ServerName>\S+)', filename)
  
  # error out here if it is a bad filename
  if not match:
    raise Exception('Filename does not have an embedded server name: \'' + 
                      filename + 
                      '\'')
  server = 'http://' + match.group('ServerName')
  
  #now get all the URL's
  with open(filename, 'rU') as f:
    fileContents = f.read()
  rawUrls = re.findall(r'GET\s(\S*puzzle\S*)\sHTTP',fileContents)
  
  #error out if the file was in the wrong format
  if len(rawUrls) <= 0: 
    raise Exception('File didn\'t include any URL\'s')
  
  #clean and assemble the final URL's
  cleanUrl = {}
  for url in rawUrls:
    if url not in cleanUrl: 
      cleanUrl[url] = server + url
  
  return sorted(cleanUrl.values(), key=second_word)
  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  
  imagedir = os.path.abspath(dest_dir)

  if not os.path.exists(imagedir):
    os.mkdir(imagedir)
  index = 0 
  local_imgs = []
  
  for img_url in img_urls: 
    print 'retrieving: ' + img_url 
    local_name = imagedir + '/img' + str(index)
    urllib.urlretrieve(img_url, local_name)
    local_imgs.append(local_name)
    index += 1
  
  html = '<verbatim>\n<html>\n<body>\n'
  for local_img in local_imgs:
    html += '<img src=\"' + local_img + '\">\n'
  html += '</body>\n</html>'
  with open(imagedir + '/index.html','w') as f:
    f.write(html)
  return
  

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])
  
  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
