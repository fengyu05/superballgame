# -*- coding:gb2312 -*-
# -*- $Id: map_gen.py 2 2009-04-20 03:10:36Z fengyu05 $ -*-

import gamectrl.const as const
import logic.brickmanager as brickmanager
import random



class MapGener(object):
	def __init__(self):
		self.girds = None
		self.wall = brickmanager.WALL_ID


	def gen(self, x, y, level=1): # level in [1,5]
		self.grids = []
		for j in xrange(y):
			self.grids.append([0] * x)
			for i in xrange(1,x-1):
				ranval = random.randint(0, self.wall - 1)
				ranval = min(int(ranval * level / 4), 5)
				self.grids[j][i] = ranval



	def output(self, filename):
		f = open(filename, "w")
		f.write("gridmap = [\n")
		for lis in self.grids:
			f.write('\t[')
			for val in lis:
				f.write('%d, '% val)
			f.write('],\n')
		f.write("]")
		f.close()



if __name__ == '__main__':
	gener = MapGener()
	gener.gen( const.GRID_NUM_X, 20, 5)
	gener.output( "lv_.py" )


