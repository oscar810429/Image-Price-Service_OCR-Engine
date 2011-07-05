#!/usr/bin/env python
"""
A minimal Quixote demo.  If you have the 'quixote' package in your Python
path, you can run it like this:

  $ python 360buy_price.py

The server listens on localhost:8080 by default.  Debug and error output
will be sent to the terminal.
"""

import os,sys,md5
import quixote
from quixote.publish import Publisher
from quixote.directory import Directory
from PIL import Image
from captchaidentifier import CaptchaIdentifier
import cookielib,StringIO, urllib, urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
from copy import copy
from quixote.http_request import HTTPRequest

_add_dot_txt_flag = True;
_tesseract_temp_path = '/tmp'
_newegg_filename_flag = 'gif'
_suning_filename_flag = 'png'

class RootDirectory(Directory):

    _q_exports = ['', 'buy360','newegg','suning']

    def _q_index(self):
        return '''<html>
                    <body>Welcome to the Quixote demo.  Here is a
                    <a href="buy360">link</a>.
                    </body>
                  </html>
                '''

    def buy360(self):
        request = quixote.get_request()
	identify = CaptchaIdentifier()
	try :
            if request.form.get("url") == None:
	    	return '0'
	    else:
		index = request.form.get("url").find("http://",0)
		if index == -1:
		    return '0'
		CAPTHA = request.form.get("url")
		cookie = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		img_file = opener.open(CAPTHA)
		tmp = StringIO.StringIO(img_file.read())
		image = Image.open(tmp)
		numbers = identify.parse(image)
		if numbers == None:
		    return '0'
		else:
		    return numbers
	except IOError:
	    return '0'

    
    def newegg(self):
	try :
	    request = quixote.get_request()
	    if request.form.get("url") == None:
		return '0'
	    newegg_url = request.environ.get('QUERY_STRING', '')
	    newegg_list = newegg_url.split('=')
	    if len(newegg_list) < 3 :
		return '0'
	    urlString = "%s=%s" % (newegg_list[1],newegg_list[2])
	    #url_params = url.decode_url_string(newegg_url)
	    #urlString = "".join(["%s=%s" % (k, v) for k, v in url_params.items()])
	    newegg = md5.new()
	    newegg.update(urlString)
	    
	    req = Request(urlString)
	    f = urlopen(req)
	    local_file = open("%s/%s.%s" %(_tesseract_temp_path,newegg.hexdigest(),_newegg_filename_flag), "w" + "b")
	    local_file.write(f.read())
	    local_file.close()
	    os.system("convert -compress none -alpha off %s/%s.%s %s/%s-convert.tiff" % (_tesseract_temp_path,newegg.hexdigest(),_newegg_filename_flag,_tesseract_temp_path,newegg.hexdigest()))
	    os.system("tesseract %s/%s-convert.tiff %s/%s" % (_tesseract_temp_path,newegg.hexdigest(),_tesseract_temp_path,newegg.hexdigest()))
	    numbers = retrieve_text("%s/%s" %(_tesseract_temp_path,newegg.hexdigest()) );
	    os.remove("%s/%s.%s" %(_tesseract_temp_path,newegg.hexdigest(),_newegg_filename_flag))
	    os.remove("%s/%s-convert.tiff" %(_tesseract_temp_path,newegg.hexdigest()))
	    os.remove("%s/%s.txt" %(_tesseract_temp_path,newegg.hexdigest()))
	    return numbers
	    if numbers == None:
		return '0'
	    else:
		return numbers
	except IOError:
	    return '0'
	


    def suning(self):
	try :
	    request = quixote.get_request()
	    if request.form.get("url") == None:
		return '0'
	    urlString = request.form.get("url")
	    newegg = md5.new()
	    newegg.update(urlString)
	    cookie = cookielib.CookieJar()
	    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	    req = Request(urlString)
	    f = urlopen(req)
	    local_file = open("%s/%s.%s" %(_tesseract_temp_path,newegg.hexdigest(),_suning_filename_flag), "w" + "b")
	    local_file.write(f.read())
	    local_file.close()
	    os.system("convert -compress none -depth 8 -alpha off %s/%s.%s %s/%s-convert.tiff" % (_tesseract_temp_path,newegg.hexdigest(),_suning_filename_flag,_tesseract_temp_path,newegg.hexdigest()))
	    os.system("tesseract %s/%s-convert.tiff %s/%s" % (_tesseract_temp_path,newegg.hexdigest(),_tesseract_temp_path,newegg.hexdigest()))
	    numbers = retrieve_text("%s/%s" %(_tesseract_temp_path,newegg.hexdigest()) );
	    os.remove("%s/%s.%s" %(_tesseract_temp_path,newegg.hexdigest(),_suning_filename_flag))
	    os.remove("%s/%s-convert.tiff" %(_tesseract_temp_path,newegg.hexdigest()))
	    os.remove("%s/%s.txt" %(_tesseract_temp_path,newegg.hexdigest()))
	    return numbers
	    if numbers == None:
		return '0'
	    else:
		return numbers
	except IOError:
	    return '0'        

def retrieve_text(scratch_text_name_root):
    if _add_dot_txt_flag:
	inf = file(scratch_text_name_root + '.txt')
    else:
	inf = file(scratch_text_name_root)
    text = inf.read().strip()
    inf.close()
    return text

def create_publisher():
    return Publisher(RootDirectory(),
                     display_exceptions='plain')


if __name__ == '__main__':
    from quixote.server.simple_server import run
    print 'creating website listening on http://192.168.1.48:8099/'
    run(create_publisher, host='192.168.1.48', port=8099)
