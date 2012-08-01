#!/bin/usr/env python

def findLink(content):
	www = 'www.'
	windex = 0 
	http = 'http'
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
						return start_end
				start_end.append(j)
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
						return start_end
				start_end.append(j)
				return start_end
		else:
			httpindex=0
	return start_end

def stripLink(content):
	start_end = findLink(content)
	if(len(start_end) == 0):
		return [content]
	else: 
		if(start_end[1] == len(content)-1):
			return [ content[:start_end[0]-1], content[start_end[0]:] ]
		else:
			return [ content[:start_end[0]-1], content[start_end[0]:start_end[1]], content[start_end[1]:] ]

def scanLinks(content):
	linksList = []
	isLink = []
	tempList = stripLink(content)
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

	# print linksList
	# print isLink
	return [linksList, isLink]

if __name__ == '__main__':
	content = """
	word0
		www.alpsayin.com word1 word2 word3
		http://www.alpsayin.com word4 word5
		word6
		www.alpsayin.com
"""
	index = findLink(content)
	print index
	print content[index[0]:]
	stripped = stripLink(content)
	print stripped
	stripped = stripLink(stripped[2])
	print stripped
	stripped = stripLink(stripped[2])
	print stripped
	print ''
	scanresults = scanLinks(content)
	print str(scanresults[0])+'\n'+str(scanresults[1])