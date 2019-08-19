nonBreakSpace = u'\xa0'
import bs4
from bs4 import BeautifulSoup
import urllib.request
import requests
import time
import re
import os
import pathlib
import datetime

cwd = os.getcwd()
baselink = "https://www.snopes.com/category/facts/page/"
verdicts = dict()

def getOnlyText(root):
	if root.string != None:
		return root.string
	else:
		return ''.join([getOnlyText(e) for e in root.contents])

def checkDone(title):
	for e in os.walk(cwd+"/snopes/"):
		if title in e[0]:
			return True

def check_title(title):
	print(title)
	if "FALSE" in title[:6]:
		return(True,"false")
	elif "TRUE" in title[:5]:
		return(True,"true")
	else:
		return(False,None)

jumped = 0
count = 0
noquote = 0

last_date = datetime.datetime.now().strftime("%y.%m.%d")
# 458 starts second template
# "jobs market" article is faulty
# 1160 total pages
for pagenumber in range(1152,1161):
	if pagenumber is 1:
		url = "https://www.snopes.com/category/facts/"
	else:	
		url = baselink+str(pagenumber)+"/"
	req = requests.get(url)
	data = req.text
	soup = BeautifulSoup(data,"html.parser")
	lwrapper = soup.find("div", {"class":"list-wrapper"})
	if(lwrapper is None):
		print("!?!?!?")
	# assert lwrapper == None
	p = lwrapper.findAll("article")
	for i in p:
		count += 1
		print("\033[H\033[J")
		title = getOnlyText(i.find("h2",{"class" : "title"}))
		regex = re.compile('[^a-zA-Z]')
		nonspace_title = regex.sub('', title)
		link = i.find("a")['href']
		 
		date = i.find("span",{"class" : "article-date"})
		if date is None:
			continue
		date = getOnlyText(date)
		if date == "Updated":
			date = last_date
		else:
			date = datetime.datetime.strptime(date, "%d %B %Y").strftime("%y.%m.%d")
		last_date = date
		print("J> {} P> {} T> {}".format(jumped,pagenumber,title))
		# # source links and htmls
		# full answer
		# verdict
		req = requests.get(link)
		data = req.text
		soup = BeautifulSoup(data,"html.parser")
		content = soup.find("div",{"class":"entry-content article-text"})
		# CONTENT
		if (content is None):
			jumped+=1; print("Content is None: ",title,jumped)
			with open(cwd+"/snopes/error_log.txt","a+") as error_log:
				error_log.write("Content is None: "+date+"."+title+"\n\n")
			continue
		# ALREADY SAVED
		if (checkDone(nonspace_title)):
			jumped+=1; print("Already saved article: ",title,jumped)
			continue

		# CLAIM
		if (content.find("div", {"class":"claim"}) is None):
			if content.p is not None:
				claim = getOnlyText(content.p)
				if "claim" not in claim.lower():
					jumped+=1; print("No \"claim\" element: {} {} \n\n".format(title,jumped))
					with open(cwd+"/snopes/error_log.txt","a+") as error_log:
						error_log.write("P> "+str(pagenumber)+" No \"claim\" element: "+date+"."+title+"\n\n")
					continue
				claim = claim.lstrip("Claim: ")
			else:
				jumped+=1; print("No \"claim\" element: {} {} \n\n".format(title,jumped))
				with open(cwd+"/snopes/error_log.txt","a+") as error_log:
					error_log.write("P> "+str(pagenumber)+" No \"claim\" element: "+date+"."+title+"\n\n")
				continue
			# VERDICT
			flag,value = check_title(soup.find("title").text)
			if flag:
				verdict = value
			elif content.find("div", {"class":"claim-old"}) is not None:
				verdict = getOnlyText(content.find("div", {"class":"claim-old"}))
			else:
				jumped+=1; print("No \"verdict\" element: {} {} \n\n".format(title,jumped))
				with open(cwd+"/snopes/error_log.txt","a+") as error_log:
					error_log.write("P> "+str(pagenumber)+" No \"verdict\" element: "+date+"."+title+"\n\n")
				continue
		else:
			if content.find("p", {"itemprop":"claimReviewed"}) is not None:
				claim = content.find("p", {"itemprop":"claimReviewed"}).text.strip()
			else:
				claim = content.p.text.strip()
			verdict = content.find("div", {"class":"claim"})['class'][1]
		
		if verdict in verdicts:
			verdicts[verdict] += 1
		else:
			verdicts[verdict] = 1
		# get the whole rest of the html:
		html = soup.new_tag('a')
		for idx,elem in enumerate(content):
			text = getOnlyText(elem).lower()
			if "origin" == text:
				c = soup.new_tag("div")
				for e in content.contents[idx:]:
					if "Contact us" in getOnlyText(e):
						break
					else:
						html.append(e)

		assert claim is not None, "Claim is None"
		assert html is not None, "HTML is None"

		

		p_path = cwd+"/snopes/"+date+"."+nonspace_title
		pathlib.Path(p_path).mkdir(parents=True, exist_ok=True)
		# save main source content, link, and verdict
		with open(p_path+"/info.txt", "w+") as of:
			of.write("Title: "+title+"\n")
			of.write("Claim: "+claim+"\n")
			of.write("Date: "+date+"\n")
			of.write("Link: "+link+"\n")
			of.write("Verdict: "+verdict+"\n\n")
			# of.write("Content: "+answer)
		with open(p_path+"/article.html", "w+") as of:
			of.write(html.prettify())
		if (html.blockquote is None):
			noquote += 1
		else:
			with open(p_path+"/origin.txt", "w+") as of:
				of.write(html.blockquote.prettify())
		# time.sleep(.4)

with open(cwd+"/c_info.txt", "a+") as of:
	of.write(str(verdicts)+"\n")
	of.write("No quote: "+str(noquote)+"\n Total: "+str(count))