#!/usr/bin/python

# This work is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

# Developed by Shashank S Rao, Rohit Varma, Sandeep R.V for Udacity CS101 contest.
# 20th April 2012.

# For help checkout the TVQuest Help Doc.

#importing modules needed
import urllib
import re
import datetime
import time
import pickle
import urllib2

# init() is used to read the channel list and index of shows from file
# it returns two dictionaries of channel list and show index.
def init():
	file = open("channellist.txt","rU")
	channel = pickle.load(file)
	file.close()
	file = open("index.txt","rU")
	db = pickle.load(file)
	file.close()
	return channel, db
	
# Channel() finds a channel dictionary from show dictionary. 
# Keys are channel names values are list of shows in the channel
def Channel(dic):
	chan={}
	for ele in dic:
		for e in dic[ele][0]:
			if e[0] not in chan:
				chan[e[0]]=[]
				chan[e[0]].append(ele)
			else:
				if ele not in chan[e[0]]:
					chan[e[0]].append(ele)
	return chan
	
# getStuff() is used to get a modified list of shows within a timegap for channel browsing
# It takes as input show details and the index
# It returns modified retails and a Boolean value. 
# The Boolean value is True is the show is on today. 
def getStuff(details,d):
	modified=[]
	day = False
	for eachchannel in details[0]:
		showtime = eachchannel[1]
		list = []
		for i in range(0,len(showtime)):
			if	datetime.datetime.now() < showtime[i]-datetime.timedelta(days=1):
				break		
			if showtime[i].strftime('%d')==datetime.datetime.now().strftime('%d') and showtime[i].strftime("%H%M")>=d.strftime("%H%M"):
				day = True
				list += [showtime[i]]
		modified +=[ [eachchannel[0],list]	]
	modified = [modified]
	modified +=[details[1],details[2]]
	return modified,day
	
# display() is the Display helper function for the channel surfer
def display(showlist,timelist):
	i=0
	for ele in timelist:
		print ele.strftime("%I:%M%p")," ",showlist[i]
		i=i+1
		
# output() takes in a dictionary of datetime objects to shownames
# used to print results with help of display() 
def output(today):
	list = []
	x= sorted(today.keys())
	l=0
	b=0
	d=datetime.datetime.now()
	for ele in x:
		if ele>d:
			if (ele-d).seconds >7200:
				break
		l=l+1
	l=l+1
	if l>len(x):
		l=len(x)
	if l>5:
		l=5
	if l==0:
		print "No more shows found."
		return -1
	
	for ele in x[:l]:
		list.append(today[ele])
	display(list,x[:l])
	if not datetime.datetime.now().strftime("%H")in [22,23]:
		return 1
	else:
		return -1
		
# makedict() Makes a dictionary of times to shownames
# This is used to print shows in increasing order of time
def makedict(d,theshows,db,channelname):
	today={}
	for ele in theshows:
		x,y=getStuff(db[ele],d)
		if y==True:
			for timings in x[0]:
				if timings[0]==channelname:
						if len(timings[1])!=0:
							for times in timings[1]:
								today[times]=ele
	return today
	
# menu() provides menu operations for the channel surfer
def menu(channel,db):
	chandic = Channel(db)
	query = raw_input("\nEnter a channel name: ")
	if len(query)<3:
		print "Too short a query."
		return
	found = {}
	i=1
	for ele in channel:
		if query.lower() in channel[ele].lower():
			if channel[ele] in chandic:
				found[i]=channel[ele]
				i=i+1
	for ele in sorted(found.keys()):
		print ele,". ",found[ele]
	if len(found.keys())==0:
		print "Not found."
		return
	ch = raw_input("Enter channel number : ")
	ch = int(ch)
	if not ch in found:
		return
	theshows = chandic[found[ch]]
	d=datetime.datetime.now()
	d=d-datetime.timedelta(hours=1)
	today = makedict(d,theshows,db,found[ch])
	print "\nThe shows on this channel currently today: "
	check = output(today)
	if check == -1:
		d=datetime.datetime.now()+datetime.timedelta(days=1)
		d=d.replace(hour=0)
		d=d.replace(minute=0)
		tomo= makedict(d,theshows,db,found[ch])
		print "\nThe shows on this channel tomorrow : "
		output(tomo)
		
# channelsurfer() is the main function for surfing channels
# handles all function calls 
def channelsurfer(cdict,db):
	while True:
		menu(cdict,db)
		ch = raw_input("\nWant to browse again? (y/n) : ")
		if ch.lower()=="n":
			break

# get Show() takes a user input i,e a show name and get's the details of show by using dictionary
# if show not in dictionary calls getlist to get a list of similar show names
# dict is the dictionary taken as parameter
def getShow(dict):
	print "Enter show name to search For "
	show = raw_input()
	if show not in dict:
		if len(show) >= 3:
			getalist(show,dict)
		else:
			option = raw_input("Invalid Search Query.\n(y) for new search and (q) to quit : ")
			if option == "q":
				return
			else:
				getShow(dict)
	else:
		details = dict[show]
		mod= getrequiredStuff(details)
		printmod(mod,show)

# getalist(), if the show name is not correct then search for shows with similar names in our 
# database, and get a list of such names
def getalist(show,dict):
	showlist = []
	for all in dict.keys():
		if show.lower() in all.lower() and all not in showlist:
			showlist += [all]			
	s = show.split()
	for all in dict.keys():
		for each in s:
			if each.lower() in (all.lower()).split() and all not in showlist:
				showlist += [all]
				break
	showall(showlist,dict)

# showall() takes the list and dictionary as the parameter prints
# prints all the list of show names and takes the user query to search for a particular
def showall(gotlist,dict):
	gotlist = optimizelist(gotlist,dict)
	if len(gotlist)==0:
		print "We are Sorry to inform that the show you are searching for is not in our database"
	else:
		print "We were unable to find an exact match of your query, please look through the list of similar show names. Hope you find your show :) "
		printshownames(gotlist,dict)
		num = input( "\nEnter the number of the show you want details else -1 to stop: ")
		while True and num != -1:
			details = dict[gotlist[num -1]]
			mod= getrequiredStuff(details)
			printmod(mod,gotlist[num-1])
			choice = raw_input( "\nWant to Continue(Y/N): ")
			if choice.lower() =="n":
				 break
			else:
				num = input( "\nEnter the number of the show you want details else -1 to stop: ")
				
# getrequiredStuff() visits each dates of all channels till it finds the showtime which is close to current
# time  and adds it to the newlist along with the channel name and new dates
def getrequiredStuff(details):
	modified=[]
	for eachchannel in details[0]:
		showtime = eachchannel[1]
		for i in range(0,len(showtime)):
			if	datetime.datetime.now() < showtime[i]:
				break
		modified +=[ [eachchannel[0],showtime[i:]]	]
	modified = [modified]
	modified +=[details[1],details[2]]
	return modified

# printshownames() prints only the shownames 
# from the list of names given also seperates from movies and TV Shows
def printshownames(gotlist,dict):
	i = 0
	flagmovies = True
	flagtvshows = True
	while i < len(gotlist):
		if i % 10 == 9:
			op = raw_input ("\n Want to Load more shows (Y/N): ")
			if op.lower() == "n":
				break
		if isMovie(gotlist[i],dict) and flagmovies:
			print "\nMovies\n"
			flagmovies = False
		elif flagtvshows and not isMovie(gotlist[i],dict):
			print "\nTV SHOWS\n"
			flagtvshows = False
		i = i+1 
		print str(i) + ": " + str(gotlist[i-1])

# printmod() prints the Channel name,info,time and date
def printmod(mod,show):
	print "\nShow Name: " +show
	print"About the Show: "+mod[1]
	print "Show Type: " + mod[2]
	for each in mod[0]:
		if len(each[1])!=0:
			print"Channel Name: " + each[0]
		for i in range(0,len(each[1])):
			if i==3:
				break
			if each[1][i].strftime('%d')== datetime.datetime.now().strftime('%d'):
				print "Show's on today at "+ each[1][i].strftime('%H:%M')
			else:
				print "Time of Show on	" + each[1][i].strftime('%m/%d/%Y')+" is "+each[1][i].strftime("%H:%M")

#optimizelist() makes the list of names as one's with movies first and TV shows later
def optimizelist(gotlist,dict):
	newlist = []
	for each in gotlist:
		if isMovie(each,dict):
			continue
		else:
			newlist.append(each)
	return newlist

# todaysHighlights() prints all the shows that comes on the day..
def todaysHighlights(dict):
	todays= shows(dict)
	listofnames = optimizelist(todays.keys(),dict)
	if len(listofnames)==0:
		print "We are Sorry no shows that are today in our database"
	else:
		print "\nTODAY'S HIGHLIGHTS\n"
		printshownames(listofnames,dict)
		num = input( "\nEnter the number of the show you want details else -1 to end: ")
		while num != -1:
			printmod(todays[listofnames[num-1]],listofnames[num-1])
			num = input( "\nEnter number if you want details of another show or -1 to end: ")

# shows() returns all the shows that are casted today as a new 
# dictionary with only today's shows as keys
def shows(dict):
	todays = {}
	for all in dict.keys():
		if isMovie(all,dict):
			continue
		details = dict[all]
		modified,day = gettodaysStuff(details)
		if day==True:
			todays[all]=modified
	return todays

# gettodaysStuff() takes the details of a particular show as a parameter and checks whether the show is on today... 
# if Yes then it return the new set of details that are the timings of show and on which channel along with a pramater day 
# which is True if it's on today and false if not
def gettodaysStuff(details):
	modified=[]
	day = False
	for eachchannel in details[0]:
		showtime = eachchannel[1]
		list = []
		for i in range(0,len(showtime)):
			if	datetime.datetime.now().strftime('%d') < showtime[i].strftime('%d'):
				break		
			if showtime[i].strftime('%d')==datetime.datetime.now().strftime('%d') and showtime[i].strftime("%H%M")>=datetime.datetime.now().strftime("%H%M"):
				day = True
				list += [showtime[i]]
		modified +=[ [eachchannel[0],list]	]
	modified = [modified]
	modified +=[details[1],details[2]]
	return modified,day

# showmovies() shows a list of only movies for user to get information of ..				
def showmovies(dict):
	movies = getMovies(dict)
	printshownames(movies,dict)
	num = input( "\nEnter the number of the movie you want details else -1 to stop: ")
	while num != -1:
		details = dict[movies[num -1]]
		mod= getrequiredStuff(details)
		printmov(mod,movies[num-1])
		num = input( "\nEnter number if you want to search for another movie or else -1 to stop: ")

# getMovies() returns a list of movies from the dict
def getMovies(dict):
	movies = []
	for ele in dict.keys():
		if isMovie(ele,dict):
			movies += [ele]
	return movies

# printmov() prints a movie name,channel name,and all timing details of the movie
def printmov(mod,name):
	print "\nMovie Name: " + name
	print "Type : " + mod[2]
	for all in mod[0]:
		print "Channel Name : " + all[0]
		for i in range(0,2):
			if i >= len(all[1]):
				break
			if all[1][i].strftime('%d')== datetime.datetime.now().strftime('%d'):
				print "Movie's today "+ all[1][i].strftime('%H:%M')
			else:
				print "Time of Show on	" + all[1][i].strftime('%m/%d/%Y')+" is "+all[1][i].strftime("%H:%M")
		print ""	

# upcomingmovies() prints all the movies that are upcoming, Most of them being today and tommorrow
def upcomingmovies(list,dict):
	newlist = []
	for ele in list:
		if ele in dict:
			newlist.append(ele)
	date = maketime(dict,newlist)
	sort=sortDate(date)
	newsort = dateCompare(sort)
	printMovies(newsort,date)
	
#printUpcoming() prints the details of the upcoming movies,
def printUpcoming(gotlist,date):
	i = 0
	j = 0
	c = 0
	f = 0
	d = datetime.datetime.now()
	while j < len(gotlist):
		if gotlist[j].strftime('%d') == d.strftime('%d'):
			if not c:
				print "\nUpcoming Movies\n"
				c=1
			for e in date[gotlist[j]]:
				if i % 10 == 9:
					return gotlist[j+i:]
				print str(i+1) + ":	 Movie Name  : " + str(e[0])
				print "	 Channel Name :  "+e[1]
				print "	 Show Time    :  " +str(gotlist[j].strftime('%H:%M'))	+ "\n"
				i = i + 1
		elif gotlist[j].strftime('%d') == (d + datetime.timedelta(days=1)).strftime("%d"):
			if not f:
				print "Coming Tomorrow\n"
				f=1
			for e in date[gotlist[j]]:
				if i % 10 == 9:
					return gotlist[j+i:]
				print str(i+1) + ":	 Movie Name	 : " + str(e[0])
				print "	 Channel Name:  "+e[1]
				print "	 Show Time   :  " +str(gotlist[j].strftime('%H:%M'))	+ "\n"
				i = i + 1
		else:
			for e in date[gotlist[j]]:
				if i % 10 == 9:
					return gotlist[j+i:]
				print str(i+1) + ":	 Movie Name :		 " + str(e[0])
				print "	   Channel Name :	   "+e[1]
				print "	   Show Date and Time: " +str(gotlist[j].strftime('%m/%d/%Y'))+","+str(gotlist[j].strftime('%H:%M')) + "\n"
				i = i + 1
		j=j+1
	return []

# printMovies() calls the printUpcoming to print the movie details
def printMovies(gotlist,date):
	while gotlist:
		gotlist=printUpcoming(gotlist,date)
		if gotlist:
			op = raw_input ("\nWant to Load more movies (Y/N) : ")
			if op.lower() == "n":
				return
			else:
				print ""

# isMovie() takes a movie name as parameter and returns true if the name is movie or else false
def isMovie(name,dict):
	details = dict[name]
	if "Film".lower() in details[2].lower():
		return True
	return False
	
# upcoming() crawls the website for the upcoming movie's and returns a list of the same
def upcoming():
	print "Looking up movies online. Please wait..."
	req = urllib2.Request("http://tvnow.in/upcomingfilms.asp")
	r = urllib2.urlopen(req)
	content= r.read()
	shows = re.findall("class=.programmeheading.>(.+)./span",content)
	newshows =[]
	for ele in shows:
		if len(ele)>3:
			newshows.append(ele)
	return newshows


# FUNCTIONS FOR INDEX CREATION 
# These are the functions needed for the crawler
# They crawl the tvnow website and create index.txt 

# makepage() returns the page that needs to be crawled
def makepage(chno,date):
	return "http://www.tvnow.in/channellisting.asp?ch="+chno+"&cTime="+date

# gethtmlfile() returns page from url
def gethtmlfile(url):
	page= urllib.urlopen(url)
	return page
	
# pageopen() builds the showlist dictionary 
# it takes as input channel number, datetime object and a dictionary to populate 
def pageopen(chno,d,showlist):
	date = d.strftime('%m/%d/%Y')
	shows = {}
	url = makepage(chno,date) 
	page = gethtmlfile(url)
	content = page.read()
	channel = re.findall("<TR><TD ><table><tr><td><span class=programmeheading>(.+)</span>",content)
	shows = re.findall("span class=.programmeheading. >(.+)./span",content)
	categories = re.findall("<span class=.tvchannel.>Category </span><span class=.programmetext.>(.+)</span></a><br>",content)
	contentinfo = re.findall("span class=.programmetext.>(.+)./span",content)
	full =[]
	for ele in contentinfo:
		if ele in categories:
			full.append("")
		else:
			full.append(ele)
	contentinfo=full
	if len(shows) == 0:
		return
	times = re.findall("span class=.tvchannel.>(.{7,8})./span",content)
	i=0
	j=0
	a=0
	list = []
	while i<len(shows):
	   if times[i][-3:-1]=="am":
		  if times[i-1][-3:-1]=="pm":
			 d = d+datetime.timedelta(days=1)
			 date = d.strftime('%m/%d/%Y')
	   s = times[i]
	   s = s[:-3]+" "+s[-3:-1].upper()
	   s = time.strftime('%H:%M:%S', time.strptime(s, '%I:%M %p'))
	   if shows[i] in showlist:
		  k=0
		  flag=False
		  for ele in showlist[shows[i]][0]:
			 if ele[0]==channel[0]:
				flag=True
				showlist[shows[i]][0][k][1].append(datetime.datetime(int(date[-4:]), int(date[:2]), int(date[3:5]), int(s[:2]), int(s[3:5]), 0, 0))
				break
			 k=k+1
		  if flag==False:
			 showlist[shows[i]][0].append([channel[0],[datetime.datetime(int(date[-4:]), int(date[:2]), int(date[3:5]), int(s[:2]), int(s[3:5]), 0, 0)]])
		  i=i+1
		  if j>=len(contentinfo):
			 break
		  else:
			 a=a+1
		  if "" != contentinfo[j]:
			 j = j+1
		  j=j+1
	   else:
		  list=[]
		  outerlist = []
		  list.append(channel[0])
		  list.append([datetime.datetime(int(date[-4:]), int(date[:2]), int(date[3:5]), int(s[:2]), int(s[3:5]), 0, 0)])
		  outerlist.append([list])
		  if j>=len(contentinfo):
				return
		  if "" != contentinfo[j]:
			 if j>=len(contentinfo):
				return
			 else:
				outerlist.append(contentinfo[j])
			 j=j+1
		  else:
			 outerlist.append("")
		  if j>=len(contentinfo):
			 return
		  else:
			 outerlist.append(categories[a])
		  a=a+1
		  showlist[shows[i]]=outerlist
		  i=i+1
		  j=j+1
			  
# index() is the function which calls other functions for index creation
# it also checks if index is valid
def index():
	showlist = {}
	print "\nChecking Index "
	file = open("version.txt","rb")
	d = pickle.load(file)
	file.close()
	if d<datetime.datetime.now():
		ch = raw_input( "Database is old. Build New? (y/n) ")
	else:
		ch = raw_input("Database is valid. Do you want build a new one ? (y/n) ")
	if ch.lower()=="n":
		print("Quitting index builder.. Loading database from file.. ")
		return
	print("Building complete index of 240 tv channels takes lot of time.")
	ch = raw_input("Want to use smaller database of 62 channels? (y/n) ")
	if ch=="n":
		file = open("channellist.txt","rU")
		data = ""
	else:
		file = open("smallchannel.txt","rU")
		data = "small"
	channels = pickle.load(file)
	file.close()
	j=0
	l=len(channels.keys())
	print("Please wait.. building index")
	for ele in channels.keys():
		d= datetime.datetime.today()
		for i in range(0,7):
			pageopen(ele,d,showlist)
			d= d+datetime.timedelta(days=1)
		print "[ ",str((j*100.00)/l)," % complete== " ,channels[ele], " done ====]"
		j=j+1
	file = open("index.txt","wb")
	pickle.dump(showlist,file)
	file.close()
	file = open("version.txt","wb")
	d = datetime.datetime.now()
	d=d+datetime.timedelta(days=6)
	pickle.dump(d,file)
	file.close()
	return
	
# check() checks if the index is upto date
def check():
	file = open("version.txt","rU")
	d = pickle.load(file)
	file.close()
	if d<datetime.datetime.now():
		print("Database is old. Quitting.")
		return False
	return True
# FUNCTIONS FOR INDEX CREATION END HERE
	
# Category() makes and returns a dictionary having Category as key and its value is the showname.
# Shows Index is taken as the parameter for the Category()
def Category(dic):
	catg={}
	for ele in dic:
		if dic[ele][-1] not in catg:
			catg[dic[ele][-1]]=[]
			catg[dic[ele][-1]].append(ele)
		else:
			if ele not in catg[dic[ele][-1]]:
				catg[dic[ele][-1]].append(ele)

	return catg			   

# sortDate() sorts the keys(date objects) of the 'date' dictionary in ascending order.
# 'date' dictionary is the parameters for dateTime().
# Returns a list of sorted keys(date objects) of the 'date' dictionary.
def sortDate(date):
	sortdate = sorted(date.keys())
	return sortdate

# dateCompare() compares the sorted list of keys with current date object(datetime.datetime.now()).
# Takes the sorted list of keys as a parameter for dateCompare().
# Returns sorted list where all the date objects are greater than current date object
# prior two hours ago(datetime.datetime.now()-datetime.timedelta(hours=2).
def dateCompare(sort):
	
	d=datetime.datetime.now()
	d = d - datetime.timedelta(hours=2)
	i=0
	while i<len(sort):
		if sort[i]>d:
			return sort[i:]
		i = i+1
	return []

# printnames() prints all the Live Sport Shows currently playing, Sport Shows which will be playing in  7 days,   
# print 9 Shows at a time and returns remaining list members to printshows()
def printnames(gotlist,date):
	i = 0
	j = 0
	c = 0
	f = 0
	d = datetime.datetime.now()
	while j < len(gotlist):
		if gotlist[j].strftime('%d') == d.strftime('%d'):
			if not c:
				print "\nToday's Sport Shows\n"
				c=1
			for e in date[gotlist[j]]:
				if i % 10 == 9:
					return gotlist[j:]
				print str(i+1) + ":	 Show Name   :	" + str(e[0])
				print "	 Channel Name:  "+e[1]
				print "	 Show Time   :  " +str(gotlist[j].strftime('%H:%M'))	+ "\n"
				i = i + 1
		else:
			if not f and i!=9:
				print "More Sport Shows\n"
				f=1
			for e in date[gotlist[j]]:
				if i % 10 == 9:
					return gotlist[j:]
				print str(i+1) + ":	 Show Name :	 " + str(e[0])
				print "	 Channel Name :	   "+e[1]
				print "	 Show Date and Time: " +str(gotlist[j].strftime('%m/%d/%Y'))+","+str(gotlist[j].strftime('%H:%M')) + "\n"
				i = i + 1
		j=j+1
	return []

# printshows() checks if Sport Live Show List is empty or not. 
# It ask the user whether he/she would want to load more shows and calls printname() accordingly.
def printShows(gotlist,date):
	while gotlist:
		gotlist=printnames(gotlist,date)
		if gotlist:
			op = raw_input ("\nWant to Load more shows (Y/N) : ")
			if op.lower() == "n":
				return
			else:
				print ""

# showSport() calls the functions (getSport(), maketime(), sortDate(), dateCompare(), printshows()) to print Live 
# Sport Shows for the user.
def showSport(dict):
	sport = getSport(dict)
	date = maketime(dict,sport)
	sort=sortDate(date)
	newsort = dateCompare(sort)
	printShows(newsort,date)

# getSport() makes a list of all the Live Sport Shows from the Shows Index.
# Shows Index is taken as the parameter for getSport() function.
# Returns a list of all the Live Sport Shows.
def getSport(dic):
	sport = []
	for ele in dic:
		if 'Live' in ele and 'Sport' in dic[ele][-1]:
			sport.append(ele)
	return sport

#  maketime() makes a dictionary 'date' having date objects as its keys and
# the values for keys are the list containing a list of the 'Live Sport Show'
# and 'The Channel its playing in'.
# Shows Index and the List of Live Sport Shows are taken as parameters for dateTime()
# function.
# Return the dictionary 'date'.
def maketime(dic,sport):
	date={}
	for ele in sport:
		for e in dic[ele][0]:
			for d in e[1]:
				if d not in date:
					date[d] = []
					date[d].append([ele,e[0]])
				else:
					if [ele,e[0]] not in date[d]:
						date[d].append([ele,e[0]])
	return date

# makeCat() divides the Category into Main Category and Sub Category (Category-> Main Category-Sub Category).
# Show index is taken as a parameters for makeCat().
# Returns a dictionary having Main Category as its key and list of Sub Categories as its value.
def makeCat(db):
	maincat = {}
	for ele in db:
		cat = db[ele][2]
		cut = cat.find("-")
		outer = cat[:cut]
		inner = cat[cut+1:]
		if outer in maincat:
			if not inner in maincat[outer]:
				maincat[outer].append(inner)
		else:
			maincat[outer] = [inner]
	return maincat

# printCat() prints the menu of Main Categories for the user.
# Show index is taken as a parameters for printCat()
# Its returns the Main category that the user has selected.
def printCat(maincat):
	key=[]
	for ele in maincat:
		key.append(ele)
	i=0
	print "\nCategories\n"
	while i<len(key):
		i = i+1
		print str(i) + ": " + str(key[i-1])
	num = input( "\nEnter the number of the category you want details else -1 to stop: ")
	if num != -1:
		return key[num-1]
	return []
	
# printSub() prints the menu of all the Sub Categories of the Main Category that is selected 
# by the user.  
# List of Sub Categories is taken as a parameters for printSub().
# Returns the Sub-Category that the user has selected.
def printSub(key):
	i=0
	print "\nSubCategories\n"
	while i<len(key):
		i = i+1
		print str(i) + ": " + str(key[i-1])
	num = input( "\nEnter the number of the sub-category you want details else -1 to stop: ")
	if num != -1:
		return key[num-1]
	return []
		
# conCat() returns the Category(Main Category-Sub Category)
def conCat(key,sub):
	cat=key+'-'+sub
	return cat

# printcatnames() prints all the TV Shows of Selected Category and Channel currently playing, 
# TV Shows which will be playing in  7 days, print 9 Shows at a time
# and returns remaining list members to printcats().
def printcatnames(gotlist,date,category,chname):
	i = 0
	j = 0
	c = 0
	f = 0
	d = datetime.datetime.now()
	print "\nShows of Category: "+category+" Played in Channel: "+chname
	while j < len(gotlist):
		if gotlist[j].strftime('%d') == d.strftime('%d'):
			if not c:
				print "\n		Today's Shows		\n"
				c=1
			if i % 10 == 9:
				return gotlist[j:]
			print str(i+1) + ":	 Show Name : " + str(date[gotlist[j]])
			print "	 Show Time : " +str(gotlist[j].strftime('%H:%M'))
			print ""
			i = i + 1
		else:
			if not f and i!=9:
				print "\n		More Shows		\n"
				f=1
			if i % 10 == 9:
				return gotlist[j:]
			print str(i+1) + ":	 Show Name		: " + str(date[gotlist[j]])
			
			print "	 Show Date and Time : " +str(gotlist[j].strftime('%m/%d/%Y'))+","+str(gotlist[j].strftime('%H:%M'))
			print ""
			i = i + 1
		j=j+1

	return []

# printcats() checks if Sport Live Show List is empty or not. 
# It ask the user whether he/she would want to load more shows and calls printcats() accordingly.
def printcats(gotlist,date,category,chname):
	while gotlist:
		gotlist=printcatnames(gotlist,date,category,chname)
		if gotlist:
			op = raw_input ("\nWant to Load more shows (Y/N) : ")
			if op.lower() == "n":
				return
	   
# catsearch calls all the functions(makeCat(), printCat(), printSub(), conCat(), printcatnames(), 
# printcats(), makedate(), makechannel(), printChan()) to print TV shows of Selected Category and Channel.
def catsearch(db):
	while True:
		maincat = makeCat(db)
		key = printCat(maincat)
		if key:
			subkey = printSub(maincat[key])
			if key and subkey:
				category=conCat(key,subkey)
				cato=Category(db)
				channel=makechannel(cato[category],db)
				shows=printChan(category,channel)
				if shows:
						date = makedate(db,channel[shows],shows)
						sort=sortDate(date)
						newsort = dateCompare(sort)
						printcats(newsort,date,category,shows)
				  
		ch = raw_input("\nWant to browse again? (y/n) : ")
		if ch.lower()=="n":
			break	
			
# makedate() makes a dictionary 'date' having date objects as its keys and
# the values for keys are the Showname 
# Shows Index and the List of Live Sport Shows are taken as parameters for dateTime()
# function.
# Return the dictionary 'date'.
def makedate(dic,sport,shows):
	date={}
	for ele in sport:
		for e in dic[ele][0]:
			for d in e[1]:
				if e[0] == shows:
					if d not in date:
						date[d] = ele
						
	return date

# makechannel() returns a dictionary having channel as keys and its value is the showname
# of selected category.
def makechannel(cat,dic):
	chan={}
	for ele in cat:
		for e in dic[ele][0]:
			if e[0] not in chan:
				chan[e[0]]=[]
				chan[e[0]].append(ele)
			else:
				if ele not in chan[e[0]]:
					chan[e[0]].append(ele)
	return chan

# printChan() prints the menu of channels playing shows of the selected category.
# Returns the ChannelName that the user has selected.
def printChan(cat,maincat):
	key=[]
	for ele in maincat:
		key.append(ele)
	i=0
	print "\n		"+cat+"		"
	print "\nChannels Playing That Category\n"
	while i<len(key):
		i = i+1
		print str(i) + ": " + str(key[i-1])
	num = input( "\nEnter the number of the channel you want details else -1 to stop: ")
	if num != -1:
		return key[num-1]
	return []

# askuser() takes the show dictionary and channel dictionary as input
# it makes calls to all menu functions of individual options
def askuser(out,cdict):
	ProcedureCalls = [getShow,todaysHighlights,showmovies]
	while True:
		option = input("\n\nTVQuest Options : \n\n Enter\n1. Surf Channels\n2. Show Search\n3. Today's Highlights\n4. Show Movies\n5. Upcoming Movies\n6. Sport Updates \n7. Categorywise Search\n8. Exit\nEnter Choice : ")
		if option > 8:
			print "Choose a proper number "
		elif option ==1:
			channelsurfer(cdict,out)
		elif option == 5:
			upcomingmovies(upcoming(),out)
		elif option == 6:
			showSport(out)
		elif option == 7:
			catsearch(out)
		elif option == 8:
			return
		else:
			ProcedureCalls[option-2](out)
		op = raw_input("Want to continue with main menu (Y/N) : ")
		if op.lower() == "n":
			break

# main() is the main function which first checks validity
# then calls askuser()
def main():
	print "\n\t\t Welcome to TVQuest"
	print "\tTV Show Guide and Information Browser\n"
	index()
	if check() == False:
		return
	cdict, db = init()
	askuser(db,cdict)
	
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()