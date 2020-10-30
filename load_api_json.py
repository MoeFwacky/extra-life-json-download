import sys
import os
import json
import datetime
import time
import inspect
import math
import random
import requests
import inspect
import urllib
import urllib.error
import urllib.request
from datetime import datetime
from time import sleep
from extra_life_config import *

try:
	if (sys.argv[1] == "--debug"):
		lineEnd = "\n"
	else:
		lineEnd = "\r"
except:
	lineEnd = "\r"

def line(): #get line number
	line = inspect.currentframe().f_back.f_lineno
	line = '%03d' % line
	return line

def clearline(): #clear line for reprinting on same line
	print("\t\t\t\t\t\t\t\t\t\t\t\t\t",end='\r')

def textline(line,text,endLine=lineEnd): #print to terminal including timestamp and line number
	if(endLine==lineEnd):
		clearline()
	print(datetime.now().strftime("%H:%M:%S")+": "+str(line)+" - " + text,end=endLine)

def api_call(url,file,etagList): #check extra life API for data, save data to file
	textline(line(),"Start of API Call Function: "+file[:-5])
	try: #only print if in debug mode
		if (sys.argv[1] == "--debug"):
			textline(line(),"URL: "+str(url))
	except:
		trash = "take me out" #literally garbage
	etagNew = [] #list to save the current etag
	teamJSON = [] #list for JSON data downloaded from the API
	loops = 0 
	needsUpdate = 0
	pages = 1
	urlCheck = url #for checking headers for a next page
	etagloop = 0
	for etag in etagList: #loop through stored etags to check the api for changes
		textline(line(),"Stored etag: "+str(etag))
		response = requests.get(urlCheck)
		textline(line(),"Response etag: "+str(response.headers['ETag']))
		if(response.headers['ETag'] != etag): #if changes is detected, set flag to update
			needsUpdate = "yes"
			textline(line(),file[:-5]+" DATA UPDATE DETECTED","\t\t\t\t\t\n")
		else:
			textline(line(),"ETAG MATCH FOUND, NO UPDATE NEEDED")
		textline(line(),"Checking for Next Page of Results")
		try: #check headers for link to the next page, if exists
			urlCheck = response.links['next']['url']		
			pages = pages + 1
			textline(line(),"Page "+str(pages)+" Detected")
			try:
				if (sys.argv[1] == "--debug"):
					textline(line(),str(response.links['next']['url']))
			except:
				trash = "take me out"
			nextPage = "true"
		except KeyError as error: #this indicates there are no more pages to cycle through
			textline(line(),"Exception Raised: "+str(error))
			textline(line(),"No Next Page Found")
			nextPage = "false"
			break
	textline(line(),"End of Etag List")
	while(nextPage == "true"): #flags new pages for update and inclusion in the list
		response = requests.get(urlCheck)
		try:
			urlCheck = response.links['next']['url']
			nextPage = "true"
			needsUpdate = "yes"
			textline(line(),file[:-5]+" DATA UPDATE DETECTED","\t\t\t\t\t\n")
			pages = pages + 1
			try:
				if (sys.argv[1] == "--debug"):
					textline(line(),str(response.links['next']['url']))
			except:
				trash = "take me out"
			textline(line(),"Page "+str(pages)+" Detected")
		except KeyError as error: #indicates end of data
			textline(line(),"Exception Raised: "+str(error))
			nextPage = "false"
			textline(line(),"End of Data")
			
#*****************************
	if(needsUpdate != "yes"):
		etagNew = etagList
		textline(line(),"No Changes to "+file)
		changes = 0
	else: #runs if flagged for updates
		while(pages >= 1):
			textline(line(),"Data Update Loop Start")
			loops = loops + 1
			textline(line(),"LOADING DATA FROM API: "+file[:-5]+", Page "+ str(loops),"\t\t\t\t\n")
			response = requests.get(url)
			etagNew.append(response.headers['ETag']) #save new etag
			req = urllib.request.Request( #prepare to grab data from API
				url, 
				data=None, 
				headers={
					'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
				}
			)
			if(loops != 1): #if not the first page, add new data list to existing data list
				textline(line(),"Appending Data")
				newData=json.load(urllib.request.urlopen(req))
				teamJSON.extend(newData)
			else: #if it is the first page, write data to new list
				textline(line(),"Writing First Page of Data")
				teamJSON=json.load(urllib.request.urlopen(req))
			now = datetime.now()
			changes = 1
			textline(line(),"needsUpdate="+str(needsUpdate))
			if(pages > 1): #if multiple pages, saves the new url for the next loop
				textline(line(),"Preparing for Next Page")
				try:
					if (sys.argv[1] == "--debug"):
						textline(line(),str(response.links['next']['url']))
				except:
					trash = "take me out"
				url = response.links['next']['url']
				#sleepForSeconds(rateLimit) #sleeps for set time to avoid overloading the API
			pages = pages - 1
#***************************
	if(teamJSON != []): #writes JSON data to file
		now = datetime.now()
		with open(file, "w") as write_file:
			json.dump(teamJSON, write_file)
		textline(line(),"DATA SAVED TO FILE: "+file,"\t\t\t\t\n\n")
	return etagNew

def sleepForSeconds(t): #sleeps for a set time with output
	while t >= 0:
		now = datetime.now()
		textline(line(),"Sleeping for " + str(t) + " seconds...","\r")
		#clearline()
		#print(now.strftime("%H:%M:%S")+": "+str(line())+" - Sleeping for " + str(t) + " seconds...", end='\r')
		if (t > 0):
			time.sleep(1)
		t = t - 1
	print("",end=lineEnd)

#EXTRA LIFE in fancy text
print("      :::::::::: :::    ::: ::::::::::: :::::::::      :::           :::        ::::::::::: :::::::::: :::::::::: ")
print("     :+:        :+:    :+:     :+:     :+:    :+:   :+: :+:         :+:            :+:     :+:        :+:         ")
print("    +:+         +:+  +:+      +:+     +:+    +:+  +:+   +:+        +:+            +:+     +:+        +:+          ")
print("   +#++:++#     +#++:+       +#+     +#++:++#:  +#++:++#++:       +#+            +#+     :#::+::#   +#++:++#      ")
print("  +#+         +#+  +#+      +#+     +#+    +#+ +#+     +#+       +#+            +#+     +#+        +#+            ")
print(" #+#        #+#    #+#     #+#     #+#    #+# #+#     #+#       #+#            #+#     #+#        #+#             ")
print("########## ###    ###     ###     ###    ### ###     ###       ########## ########### ###        ########## ")
print("LOAD DATA FROM EXTRA LIFE API AND SAVE TO FILE")
etagTeam = ["TEAM"]
etagTeamParticipants = ["TEAMPARTICIPANTS1"]
etagTeamDonations = ["DONATIONS1","DONATIONS2"]
while True:
	try:
#Load team participant data
		print("",end=lineEnd)
		try: 
			etagTeamParticipants = api_call(teamParticipants,teamParticipantsFile,etagTeamParticipants)
		except urllib.request.URLError as err:
			print(err)
			sleepForSeconds(rateLimit)
			etagTeamParticipants = api_call(teamParticipants,teamParticipantsFile,etagTeamParticipants)
#load team data
		print("",end=lineEnd)
		try: 
			etagTeam = api_call(team,teamFile,etagTeam)
		except urllib.request.URLError as err:
			print(err)
			sleepForSeconds(rateLimit)
			etagTeam = api_call(team,teamFile,etagTeam)
#Load donations data
		print("",end=lineEnd)
		try: 
			etagTeamDonations = api_call(teamDonations,teamDonationsFile,etagTeamDonations)
		except urllib.request.URLError as err:
			print(err)
			sleepForSeconds(rateLimit)
			etagTeamDonations = api_call(teamDonations,teamDonationsFile,etagTeamDonatoins)
		sleepForSeconds(rateLimit)
	except KeyboardInterrupt:
		textline(line(),"SCRIPT HALTED [ctrl+C]")
		sys.exit()