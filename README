TVQUEST: TV Show guide and information browser
===============================================

### What is TVQuest? ###

TV Quest allows one to 

* Surf through a channel and get the shows timings.
* Find out about Upcoming movies,Sports Shows and many more.

---

### TO DO ###

* fix broken index creator
* divide project into modules
* create documentation
* create gui/ host online using appengine

---

### Setting Up Database ###

* On running the tvquest.py user would be asked to update the database
* In case of people with limited download limit or slower speed, you can still provide yes and choose to update a smaller index of 60 channels.
* Once the database is updated you can use for a week long period without updating.

---

### User Options ###

User is given few options on running the file and based on what the user is searching for he can make his choice
The interface is very intuitive you can easily get the hang of it when you use it couple of times.

---

### How it is implemented ###

The essential part of the project is the index building.Index of tv shows is built by crawling tvnow.in with results powered by whatsonindia. We go through 7 days worth of page listings The crawled index is stored as a dictionary where

`dict[showname] -> [[channel1, [time1, time2, time3, time4...], [channel2, [time1, time2, time3, time4...]... ]], showinfo, showcategory] .`

 The dictionary is saved to file using the pickle module.

The dictionary is later reversed for categorywise search and channelsearching. (We checked robots.txt for tvnow.in and they imposed no restrictions.)

---

### Legal Stuff ###

This work is licensed under the
Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.


NOTE: TV show listings and show details of India only.

Developed by 
* Sandeep R.V
* Shashank S Rao
* Rohit Varma 

for Udacity CS101 contest 20th April 2012.

