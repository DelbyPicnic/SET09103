# Python DataObject System - Read Data
# Gordon Swan - Edinburgh Napier University

# Open file
# Read all data in the file into a string
# Parse string for JSON objects

import json, sys

def getData():
	try:
		openFile = open("data.JSON","r")
		fileData = openFile.read()

		allData = json.loads(fileData)
		return allData
	except ValueError:
		print("Coundn't parse file data: ", sys.exc_info()[0])
		raise
	except:
		print("Unexpected error when reading file: ", sys.exc_info()[0])
		raise


# Testing
print(getData()['bvx1c8']['img_views'])

