from PIL import Image,ImageDraw,ImageEnhance,ImageFilter
from fratures_360buy import FEATURES

class CaptchaIdentifier():
    def __init__(self):
        pass
    
    def parse(self, img):
        #im = img.filter(ImageFilter.CONTOUR).convert('1')
	im = img.convert("L")
	threshold = 150
	table = []
	for i in range(256):
		if i < threshold:
		    table.append(0)
		else:
		    table.append(255)

	im = im.point(table, "1")
	size = img.size[0]
	
	if img.size[0] == 60:
		blocks = [list(im.crop(b).getdata()) for b in [(20,4,29,15)]]
		return '%s' % tuple([self.identify_number(b) for b in blocks])
	elif (img.size[0]==70):
		blocks = [list(im.crop(b).getdata()) for b in [(20,4,29,15),(31,4,40,15)]]
		return '%s%s' % tuple([self.identify_number(b) for b in blocks])
	elif (img.size[0]==81):
		blocks = [list(im.crop(b).getdata()) for b in [(20,4,29,15),(31,4,40,15),(42,4,51,15)]]
		return '%s%s%s' % tuple([self.identify_number(b) for b in blocks])
	elif (img.size[0]==97):
		blocks = [list(im.crop(b).getdata()) for b in [(20,4,29,15),(31,4,40,15),(42,4,51,15),(53,4,62,15)]]
		return '%s%s%s%s' % tuple([self.identify_number(b) for b in blocks])
	elif (img.size[0]==110):
		blocks = [list(im.crop(b).getdata()) for b in [(20,4,29,15),(31,4,40,15),(42,4,51,15),(53,4,62,15),(64,4,73,15)]]
		return '%s%s%s%s%s' % tuple([self.identify_number(b) for b in blocks])
		
    def parse_newegg(self, img):
        im = img.filter(ImageFilter.CONTOUR).convert('1')
	#im = img.convert("L")
	threshold = 150
	table = []
	for i in range(256):
		if i < threshold:
		    table.append(0)
		else:
		    table.append(255)

	im = im.point(table, "1")
	size = img.size[0]
	
	if img.size[0] == 60:
		blocks = [list(im.crop(b).getdata()) for b in [(20,4,29,15),(31,4,40,15)]]
		return '%s%s' % tuple([self.identify_number(b) for b in blocks])
	elif (img.size[0]==75):
		blocks = [list(im.crop(b).getdata()) for b in [(20,4,29,15),(31,4,40,15),(15,4,51,15)]]
		return '%s%s%s' % tuple([self.identify_number(b) for b in blocks])	
	elif (img.size[0]==100):
		blocks = [list(im.crop(b).getdata()) for b in [(20,4,29,15),(31,4,40,15), (47,4,56,15), (58,4,67,15)]]
		return '%s%s%s%s' % tuple([self.identify_number(b) for b in blocks])		
		
    def parse_suning(self, img):
        im = img.filter(ImageFilter.CONTOUR).convert('1')
	#im = img.convert("L")
	threshold = 150
	table = []
	for i in range(256):
		if i < threshold:
		    table.append(0)
		else:
		    table.append(255)

	im = im.point(table, "1")
	size = img.size[0]
	
	if img.size[0] == 60:
		blocks = [list(im.crop(b).getdata()) for b in [(20,4,29,15),(31,4,40,15)]]
		return '%s%s' % tuple([self.identify_number(b) for b in blocks])
	elif (img.size[0]==75):
		blocks = [list(im.crop(b).getdata()) for b in [(20,4,29,15),(31,4,40,15),(15,4,51,15)]]
		return '%s%s%s' % tuple([self.identify_number(b) for b in blocks])	
	elif (img.size[0]==100):
		blocks = [list(im.crop(b).getdata()) for b in [(20,4,29,15),(31,4,40,15), (47,4,56,15), (58,4,67,15)]]
		return '%s%s%s%s' % tuple([self.identify_number(b) for b in blocks])
	
	
		
    def list_distance(self, m, n):
        len_plus = lambda x: len(x) + 1
       
        c = [[i] for i in range(0, len_plus(m))]
        c[0] = [j for j in range(0, len_plus(n))]
        for i in range(0, len(m)):
            for j in range(0, len(n)):
                c[i+1].append(
                    min(
                        c[i][j+1] + 1,
                        c[i+1][j] + 1,
                        c[i][j] + (0 if m[i] == n[j] else 1)
                    )
                )
        return c[-1][-1]

    def identify_number(self, source):
        distance = [self.list_distance(source, i) for i in FEATURES]
        minimal = min(distance)
        return distance.index(minimal)