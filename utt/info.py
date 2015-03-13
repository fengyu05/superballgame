# -*- coding:gb2312 -*-
# -*- $Id: info.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-
def info(o,all=False):
	print type(o)
	for v in o.__class__.__dict__:
		if all or (not v.startswith('__')) :
			tmp = o.__getattribute__(v)
			if callable(tmp):
				print 'callable : ',v
			else:
				print v

if __name__ == '__main__':
	dict={}
	info(dict)
