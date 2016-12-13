# -*- coding: utf-8 -*-

from PIL import Image
#from PIL import PixcelAcess

def scanPic():
	im = Image.open(u'1.jpg')
	backcolor = im.getpixel((0,0))
	print 'backcolor :' + str(backcolor)
	for k in xrange(im.size[0]):
		for i in xrange(im.size[1]):
			if k > 1000:
				im.putpixel((k, i),(255, 0, 0))
	brokenpic = False
	frontcolor =(0,0,0)
	masscolor = (0,0,0)
	masslines = 0
	for k in xrange(im.size[0]):
		if im.getpixel((k,i)) != backcolor:
			masscolor = im.getpixel((k,i))
		else:
			continue
		for i in xrange(im.size[1]):
			if im.getpixel((k,i)) != masscolor:
				continue
		masslines += 1
		if masslines > 50:
			brokenpic = True
			print 'Broken pic detected.'
			break
if __name__ == '__main__':
	scanPic()