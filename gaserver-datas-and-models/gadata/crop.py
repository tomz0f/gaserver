import xmltodict, os, glob
from PIL import Image
xmllsit = glob.glob('*.xml')

for i in xmllsit:
	print(i)
	with open(i, 'r', encoding='utf-8') as file:
		my_xml = file.read()
	my_dict = xmltodict.parse(my_xml)
	img = Image.open(my_dict['annotation']['filename'])
	print(my_dict)
	#img2 = img.crop((int(my_dict['annotation']['object']['bndbox']['xmin']),int(my_dict['annotation']['object']['bndbox']['ymin']),int(my_dict['annotation']['object']['bndbox']['xmax']),int(my_dict['annotation']['object']['bndbox']['ymax'])))
	#img2.save(my_dict['annotation']['filename'])
