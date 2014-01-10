import praw
from sys import argv
from time import sleep
from collections import deque
import re

noMod = False
if "--no-mod" in argv:
	noMod = True

done = deque(maxlen=200)

USERAGENT = "Imgur_link_scraper version 1.0 by /u/thirdegree"
r = praw.Reddit(USERAGENT)
SUBREDDIT = raw_input("What subreddit? If multiple, seperate by '+' (no spaces)\n> ")

def _login():
	USERNAME = raw_input("Username?\n> ")
	PASSWORD = raw_input("Password?\n> ")
	r.login(USERNAME, PASSWORD)

Trying = True
while Trying:
	try:
		_login()
		Trying = False
	except praw.errors.InvalidUserPass:
		print "Invalid Username/password, please try again."

mods = r.get_moderators(SUBREDDIT)

def pull_links(body, author):
	body = re.sub("[\(\)]", " ", body).split()
	for word in body:
		if "imgur.com" in word:
			if not noMod or (noMod and author not in mods):
				with open("Image_links.txt", "a") as links:
					links.write(word+"\n")


running = True
while running:
	mail = r.get_mod_mail()
	for message in mail:
		if message.id not in done:
			done.append(message.id)
			pull_links(message.body, message.author)
	sleep(5)
