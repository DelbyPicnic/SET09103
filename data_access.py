# Python DataObject System - Read, Write, Append, Search
# Gordon Swan - Edinburgh Napier University

import json, sys

# Method to retrieve all the data from the JSON file in one go
def getData():
	try:
		openFile = open("static/data/fileData.JSON","r")
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

# Method to get all the user account data from the JSON file in one go
def getUsers():
	try:
		openFile = open("static/data/userData.JSON","r")
		fileData = openFile.read()

		allUsers = json.loads(fileData)
		openFile.close()

		return allUsers

	except ValueError:
		print("Coundn't parse file data: ", sys.exc_info()[0])
		raise
	except:
		print("Unexpected error when reading file: ", sys.exc_info()[0])
		raise

# Method to return a specified quantity subset of data from the larger dataset
def getDataQ(count):
	try:
		rCount = int(count)
		indexer = 0;
		reqRec = {}
		allData = getData()

		for key in allData.keys():
			if indexer < rCount:
				reqRec[key] = allData[key]
			else:
				break
			indexer += 1

		return reqRec

	except ValueError:
		print("Request record count must be an int greater than 0")

# Method to return an exact record of data if it exists
def getRecord(recID):
	try:
		allData = getData()
		reqRec = allData[recID]

		return reqRec

	except ValueError:
		print("Requested record could not be found: ", sys.exc_info()[0])
		return
	except:
		print("Unexpected error occured: ", sys.exc_info()[0])

# Method to return an exact user based on a username if it exists
def getUser(uName):
	try:
		allUsr = getUsers()
		acc = allUsr[uName]

		return acc		

	except ValueError:
		print("Request data was incorrect: ", sys.exc_info()[0])
		return
	except KeyError:
		print("Requested account could not be found: ", sys.exc_info()[0])
		return
	except:
		print("Unexpected error occured: ", sys.exc_info()[0])
		return

# Method to return all the featured images
def getFeatured():
	reqRec = {}
	allData = getData()

	for i in list(allData.keys()):
		if allData[i]["img_feat"]:
			reqRec[i] = allData[i]

	return reqRec

# Method to write a dictionary of data to the JSON file
# WARNING: This method will OVERWRITE ALL DATA in the JSON file, if there is non-backed data in the file,
# this method could be lethal!
def putData(data):
	try:
		openFile = open("static/data/fileData.JSON","w")
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
			if data[i]["img_tags"] == "":
				raise ValueError("Image must have at least one tag")

	except ValueError:
		isValid = False
		raise

	if isValid == True:	
		# Append/amend all new data and try to write out to file
		try:
			allData = getData()

			for i in list(data.keys()):
				allData[i] = data[i]

			putData(allData)

			return
		except ValueError:
			print("Coundn't write file data: ", sys.exc_info()[0])
			raise

		except:
			print("Unexpected error when writing file: ", sys.exc_info()[0])
			raise

# Method to change 'featured' attribute for a record
def toggleFeat(imageID):
	allData = getData()

	for i in list(allData.keys()):
		if i == imageID:
			if allData[i]["img_feat"]:
				allData[i]["img_feat"] = False
			else:
				allData[i]["img_feat"] = True

			putData(allData)
			return True

	return False

# Method to search all of the stored data, returning records where the search terms are found in the tags
def searchData(sTerm):
	sKeys = sTerm.lower().split(" ")

	allData = getData()
	resData = {}

	# Detect wildcard - If a single star is submitted as a search key, return everything
	if "*" in sKeys:
		return allData

	for i in list(allData.keys()):
		tKeys = allData[i]["img_tags"].lower().split(" ")
		matchKeys = []

		for sKey in sKeys:
			if sKey in tKeys:
				if sKey not in matchKeys:
					matchKeys.append(sKey)
		if len(matchKeys) > 0:
			rec = allData[i]
			rec["res_rel"] = len(matchKeys) # Apply a relavence value to this item in relation to the search
			resData[i] = rec

	return resData

# A more complete search method however this method is slower as searches are essentially performed twice
def completeSearchData(sTerm):
	sKeys = sTerm.lower().split(" ")

	allData = getData()
	resData = {}

	# Detect wildcard - If a single star is submitted as a search key, return everything
	if "*" in sKeys:
		return allData

	for i in list(allData.keys()):
		tKeys = allData[i]["img_tags"].lower().split(" ")
		matchKeys = []
		dMatches = 0
		ndMatches = 0

		for sKey in sKeys:
			if sKey in tKeys:
				if sKey not in matchKeys:
					matchKeys.append(sKey)
					dMatches += 1			# A direct match was found

			if sKey in allData[i]["img_tags"].lower():
				if sKey not in matchKeys:
					matchKeys.append(sKey)
					ndMatches += 1			# An indirect match was found

		if len(matchKeys) > 0:
			rec = allData[i]
			rec["res_rel"] = (dMatches*2) + ndMatches	# Direct match keys have double relavence value
			resData[i] = rec

	return resData

