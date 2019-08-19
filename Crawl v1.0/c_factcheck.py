nonBreakSpace = u'\xa0'
from bs4 import BeautifulSoup
import urllib.request
import requests
import time
import re
import os
import pathlib
cwd = os.getcwd()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256'
baselink = "https://www.factcheck.org/fake-news/page/"
yes = 0
no = 0
verdicts = {"No":0, "Yes":0, "?":0} 
def getOnlyText(root):
	if root.string != None:
		return root.string
	else:
		return ''.join([getOnlyText(e) for e in root.contents])
def getVerdict(text):
	answer = ''.join(text.split("A:")[1:]).strip(" ")
	verdict = answer.split(".")[0][:2]
	if verdict not in ["No","Yes"]:
		verdict = "?" 
	return verdict
def getAnswerAndSources(content):
	answer = ""
	sources = []
	f_answer = 0
	f_source = 0
	contents_list = content.contents[1:-1]
	for p in contents_list:
		text = getOnlyText(p)
		if (f_answer == 1) and (f_source == 0):
			answer += text
		elif (f_answer == 1) and (f_source == 1):
			source_ref = text
			source_link = None
			if p.find("a") != None: 
				source_link = p.find("a")['href'] 
			sources.append((source_ref,source_link))
		if "full answer" == text.lower():
			f_answer = 1
		if "sources" == text.lower():
			f_source = 1
	return answer,sources
myid = 0
for pagenumber in range(1,12):
	url = baselink+str(pagenumber)+"/"
	req = requests.get(url)
	data = req.text
	soup = BeautifulSoup(data,"html.parser")
	p = soup.findAll("article")
	for i in p:
		myid += 1
		title = i.find("h3", {"class" : "entry-title"}).find("a").text
		print("\n\nP> {} T> {} ".format(pagenumber,title))
		link = i.find("h3", {"class" : "entry-title"}).find("a")['href']
		verdict = getVerdict(i.find("div", {"class" : "entry-content"}).text.replace(nonBreakSpace, ''))
		verdicts[verdict] += 1
		# get info of candidate fact
		# checked date
		# checking question
		# full answer
		# source links and htmls
		req = requests.get(link)
		data = req.text
		soup = BeautifulSoup(data,"html.parser")
		date = soup.find("time", {"class": "entry-date"}).text
		content = soup.find("div", {"class":"entry-content"})
		answer, sources = getAnswerAndSources(content)
		# make dir for each link
		regex = re.compile('[^a-zA-Z]')
		title = regex.sub('', title)
		p_path = cwd+"/factcheck/"+str(myid)+"."+title
		pathlib.Path(p_path).mkdir(parents=True, exist_ok=True)
		
		# save main source content, link, and verdict
		with open(p_path+"/info.txt", "w+") as of:
			of.write("Title: "+title+"\n")
			of.write("Date: "+date+"\n")
			of.write("Link: "+link+"\n")
			of.write("Verdict: "+verdict+"\n\n")
			of.write("Content: "+answer)
		with open(p_path+"/sources.txt", "w+") as of:
			for line in sources:
				of.write("Title:"+str(line[0])+"\nLink:"+str(line[1])+"\n\n")
	time.sleep(.4)
print(verdicts)
