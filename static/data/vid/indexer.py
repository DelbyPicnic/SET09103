import json, sys
from string import ascii_lowercase
from random import choice
from os import walk

print(''.join(choice(ascii_lowercase) for i in range(12)))


fNames = []
for (dirpath, dirnames, filenames) in walk("/home/gordon/Desktop/UNI 2017-18/Advanced Web Technologies/Coursework/SET09103/static/data/vid/"):
    fNames.extend(filenames)
    break

dataOut = {}

for f in fNames:
	if ".mp4" in f:
		isUnique = False
		id = ''
		while(isUnique == False):
			id = ''.join(choice(ascii_lowercase) for i in range(6))
			if id not in dataOut.keys():
				isUnique = True
		dataOut[id] = {
			"img_link":f,
			"img_own":"Imgur",
			"img_desc":"This image was taken from Imgur.com",
			"img_views":"0",
			"img_tags":"cinemagraph video"
		}

openFile = open("data.JSON","w")
serialisedData = json.dumps(dataOut)
openFile.write(serialisedData)
openFile.close()