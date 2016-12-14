# -*- coding: utf-8 -*-

from PIL import Image
import os
#from PIL import PixcelAcess

def scanPic(filename):
	im = Image.open(filename)
	backcolor = im.getpixel((0,0))
	#print 'backcolor :' + str(backcolor)
	#print im.size
	'''
	for k in xrange(im.size[0]):
		for i in xrange(im.size[1]):
			if i > 200:
				im.putpixel((k, i),(255, 0, 0))

	im.save('2.jpg')
	'''
	# 坏图标记
	brokenpic = False
	masscolor = (0,0,0)
	# 色块的大小
	masslines = 0
	for k in xrange(im.size[1]):
		if im.getpixel((0, k)) != backcolor:
			masscolor = im.getpixel((0, k))
			#print masscolor
		else:
			#print k
			continue
		for i in xrange(im.size[0]):
			if im.getpixel((i, k)) != masscolor:
				break
			elif i == im.size[0]-1:
				#print 'massline:{0},{1}'.format(i,k)
				masslines += 1

		if masslines > 50:
			brokenpic = True
			filename = filename.split(u'\\')[-1]
			print 'broken picture detected:  {0} '.format(filename.encode('utf-8'))
			#print 'deleting...'
			#deletefile(filename)
			break
	#print str(masslines) +':' + str(brokenpic)

def explore(dir):
	for root,dir,files in os.walk(dir):
		for file in files:
			filename = os.path.join(root,file)
			#print filename
			scanPic(filename)

def deletefile(filename):
	'''
	:param filename: 绝对地址
	:return:
	'''
	#print type(filename)
	os.remove(filename)
	print filename + ' deleted'
if __name__ == '__main__':
	#filename = u'D:\\git\\PyCrawler\\brokenPicFilter\\慧聪图片数据\\3.jpg'
	dir = u'D:\\git\\PyCrawler\\brokenPicFilter\\慧聪图片数据'
	explore(dir)
	#scanPic(filename)
	#deletefile(filename)
