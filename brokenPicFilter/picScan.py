# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os
#from PIL import PixcelAcess

def scanPic(filename):
	try:
		im = Image.open(filename)
	except:
		print filename + ' cannot open'
		return True
	#print filename
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
	if brokenpic:
		return True
	else:
		return False

def explore(dir):
	cnt = 0
	for root,dir,files in os.walk(dir):
		for file in files:
			filename = os.path.join(root,file)
			#print filename
			scanPic(filename)
			if scanPic(filename):
				cnt += 1
	print 'total broken:' + str(cnt)


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
	dir = u'C:\\Users\\zw\\Desktop\\图片地址\\慧聪网图片地址1'
	explore(dir)
	#scanPic(filename)
	#deletefile(filename)
