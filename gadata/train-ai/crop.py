import xmltodict, os, glob, pprint
from PIL import Image

xmllsit = glob.glob('*.xml')

for i in xmllsit:
	print(i)
	with open(i, 'r', encoding='utf-8') as file:
		my_xml = file.read()
	my_dict = xmltodict.parse(my_xml)
	img = Image.open(my_dict['annotation']['filename'])
	#print(my_dict)
	print(my_dict)
	try:
		img2 = img.crop((int(my_dict['annotation']['object']['bndbox']['xmin']),int(my_dict['annotation']['object']['bndbox']['ymin']),int(my_dict['annotation']['object']['bndbox']['xmax']),int(my_dict['annotation']['object']['bndbox']['ymax'])))
		img2.save(my_dict['annotation']['filename'])
		
	except:
		o= 0
		for object in my_dict['annotation']['object']:
			print(object)
			img2 = img.crop((int(object['bndbox']['xmin']),int(object['bndbox']['ymin']),int(object['bndbox']['xmax']),int(object['bndbox']['ymax'])))
			img2.save(str(o)+my_dict['annotation']['filename'])
			print(o)
			o+=1

