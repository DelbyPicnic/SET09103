# Python DataObject System - Read Data
# Gordon Swan - Edinburgh Napier University

# Open file
# Read all data in the file into a string
# Parse string for JSON objects

import json, sys

# Method to retrieve all the data from the JSON file in one go
def getData():
	try:
		openFile = open("data.JSON","r")
		fileData = openFile.read()

		allData = json.loads(fileData)
		openFile.close()

		return allData
	except ValueError:
		print("Coundn't parse file data: ", sys.exc_info()[0])
		raise
	except:
		print("Unexpected error when reading file: ", sys.exc_info()[0])
		raise

# Method to write a dictionary of data to the JSON file
# WARNING: This method will OVERWRITE ALL DATA in the JSON file, if there is non-backed data in the file,
# this method could be lethal!
def putData(data):
	try:
		openFile = open("data.JSON","w")
		serialisedData = json.dumps(data) 	# ADD VALIDATION HERE
		openFile.write(serialisedData)				# IF INVALID DO NOT PROCEED WITH WRITE!
		openFile.close()

		return
	except ValueError:
		print("Coundn't write file data: ", sys.exc_info()[0])
		raise

	except:
		print("Unexpected error when writing file: ", sys.exc_info()[0])
		raise

# Method to add data to the JSON file (SAFE) This method will read data first, before amending or appending
# to the JSON file
def addData(data):
	# Verify incoming data is in the correct format
	isValid = True
	try:
		for i in list(data.keys()):
			if data[i]["img_link"] == "":
				raise ValueError("Image permalink can't be null")
			if data[i]["img_own"] == "":
				raise ValueError("Image owner can't be null")
			if data[i]["img_desc"] == "":
				raise ValueError("Image description can't be null")
			if data[i]["img_views"] == "":
				raise ValueError("Image viewcount can't be null")
			if data[i]["img_tags"] == "":
				raise ValueError("Image must have at least one tag")

	except ValueError:
		isValid = False
		raise

	
	if isValid == True:	
		# Append/amend all new data and try to write out to file
		try:
			openFile = open("data.JSON","r")
			fileData = openFile.read()

			allData = json.loads(fileData)
			openFile.close()

			return
		except ValueError:
			print("Coundn't write file data: ", sys.exc_info()[0])
			raise

		except:
			print("Unexpected error when writing file: ", sys.exc_info()[0])
			raise

d = getData()
putData(d)


