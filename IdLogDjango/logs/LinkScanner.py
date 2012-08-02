#!/bin/usr/env python


www = 'www.'
http = 'http'
	
def findLink(content):
	"""
	findLink(content):
		parms:
			content: a string to be scanned
		returns:
			start_end: a list with two indexes indicating
			the start and end indexes of the first found link.
			If no link is found then, an empty list is returned	
	"""
	windex = 0 
	httpindex = 0
	start_end = []
	for i in range(len(content)):
		if( content[i] == www[windex] ):
			windex+=1
			if(windex == len(www)):
				start_end.append(i-len(www)+1)
				for j in range(i, len(content)):
					if(content[j].isspace()):
						start_end.append(j)
						start_end.append(www)
						return start_end
				start_end.append(j+1)
				start_end.append(www)
				return start_end
		else:
			windex=0
		if( content[i] == http[httpindex] ):
			httpindex+=1
			if(httpindex == len(http)):
				start_end.append(i-len(http)+1)
				for j in range(i, len(content)):
					if(content[j].isspace()):
						start_end.append(j)
						start_end.append(http)
						return start_end
				start_end.append(j+1)
				start_end.append(http)
				return start_end
		else:
			httpindex=0
			
	return start_end

def stripLink(content):
	"""
	stripLink(content):
		parms:
			content: string to be stripped into links and non-links
		returns:
			striplist:	If no link is found then the content itself is returned in a list.
			If a link is found in the string and it's the end of the string
			then a list with two elements is returned, first one being the non-links
			second one being the link.
			If a link is found in the string and it's NOT the end of the string
			then a list with three elements is returned, first one being the non-links
			second one being the link and the third one being the rest of the string.
	"""
	striplist = []
	start_end = findLink(content)
	# print start_end
	if(len(start_end) == 0):
		striplist.append(content)
		return striplist
	else: 
		if(start_end[0] == 0): #if content starts with link
			striplist.append('') #append empty string to beginning
			if(start_end[1] == len(content)): #if content starts and ends with link
				if(start_end[2] == www): #if the match is a www append a http:// to the beginning of the link
					content = 'http://'+content
				striplist.append(content) #append the link itself
				return striplist
		if(start_end[1] == len(content)): #if content ends with link
			striplist.append(content[:start_end[0]]) #append the non-link
			link = content[start_end[0]:start_end[1]]
			if(start_end[2] == www): #if the match is a www append a http:// to the beginning of the link
				link = 'http://'+link
			striplist.append(link) #append the link
		else:
			if(start_end[0] != 0):
				striplist.append(content[:start_end[0]])
			link = content[start_end[0]:start_end[1]]
			if(start_end[2] == www): #if the match is a www append a http:// to the beginning of the link
				link = 'http://'+link
			striplist.append(link)
			striplist.append(content[start_end[1]:])

	return striplist

def scanLinks(content):
	"""
	scanLinks(content):
		parms:
			content: string to be analyzed and stripped into links and non-links
		returns:
			A list containg linksList and isLink lists
				linksList:
					An ordered string list of stripped strings of the content. If the
					strings in this list are concataneted in the natural order, the content
					can be built without modification
				isLink:
					An ordered boolean list indicating whether the string in i'th index of
					the linksList is a link or not
	"""
	linksList = []
	isLink = []
	tempList = stripLink(content)
	# print "templist = " + str(tempList)	
	while(len(tempList) != 1):
		if(len(tempList) == 2):
			linksList.extend(tempList)
			isLink.append(False)
			isLink.append(True)
			# print linksList
			# print isLink
			return [linksList, isLink]
		else:
			if(len(tempList) == 3):
				linksList.extend(tempList[:2])
				isLink.append(False)
				isLink.append(True)
				tempList = stripLink(tempList[2])
				# print "templist = " + str(tempList)

	linksList.extend(tempList)
	isLink.append(False)

	# print linksList
	# print isLink
	return [linksList, isLink]

if __name__ == '__main__':
	content = """www.0.com www.1.com"""

	scanresults = scanLinks(content)
	print str(scanresults[0])+'\n'+str(scanresults[1])