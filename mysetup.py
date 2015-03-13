# -*- coding:gb2312 -*-
# -*- $Id: mysetup.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-


from distutils.core import setup
import glob
import py2exe

from distutils.core import setup
import py2exe


class Target(object):
	def __init__(self, **kw):
		self.__dict__.update(kw)
		self.version = '0.1'
		self.company_name = 'netease'
		self.copyright = 'netease'
		self.name = 'Super Ball'


super_ball = Target(
		 description = u'create by feng and mygoddes',
		 script = 'main.py',
		 icon_resources= [(1, "favicon.ico")]
		           )


setup(version = '0.0',
	  description = u'create by feng and mygoddes',
	  name = 'Super Ball',

	  windows = [super_ball],
	  zipfile = None,
	  options = {'py2exe':
		 	               {'bundle_files': 1,
	  					    'compressed': 1,
							}
				}
	)
