import re
from boilerpipe.extract import Extractor
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from langdetect import detect
import unicodedata
import eatiht
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import requests
import os
import eventlet
eventlet.monkey_patch()

def logError(text):
	with open(cwd+"/logfile_p.txt","r+") as log: 
		lines = log.readlines()
		for l in lines:
			if text in l:
				return
	with open(cwd+"/logfile_p.txt","a+") as log: 
		log.write(text)

def tryContent(req):
	data = req.text
	soup = BeautifulSoup(data,"html.parser")
	try0 = soup.find("div",{"itemprop":"articleBody"})
	try1 = soup.find("div",{"class":"entry-content article-text"})
	try2 = soup.find("div",{"class":"article-text"})
	try3 = soup.find("div",{"class":"entry-content"})
	catch = next((item for item in [try0, try1,try2,try3] if item is not None),soup.new_tag('div'))
	while catch.find(["applet","code","embed","head","object","script","server"]):
		catch.find(["applet","code","embed","head","object","script","server"]).decompose()

	return unicodedata.normalize('NFKD', catch.text.replace("\n","")).encode('ascii','ignore')

def bestMethod(url,req):
	eat = ''
	pipe = ''
	manual = ''
	if url[-4:] in [".jpg",".pdf",".mp3",".mp4"]:
		logError("FORMAT: "+claim_source_url+"\n")
		return ("","format")
	try:
		eat = eatiht.extract(url).replace("\n","")
	except:
		pass
	try:
		pipe = Extractor(extractor='ArticleExtractor', url=url).getText().replace("\n","")
	except:
		pass
	# try:
	manual = tryContent(req)
	# except:
		# pass
	return max([(eat,"eat"),(pipe,"pipe"),(manual,"manual")], key=lambda x: len(x[0]))

#__________________________________________________________________________________________
#_______________________________________ ****** ___________________________________________
#__________________________________________________________________________________________

cwd = os.getcwd()
parent = os.path.abspath('..')

# data_e = pd.read_csv(parent+'/input/emergent2.csv', sep='\t')
data_p = pd.read_csv(parent+'/input/politifact2.csv', sep='\t')
# data_s = pd.read_csv(parent+'/input/snopes2.csv', sep='\t')

header = ["page", "claim", "claim_label", "tags", "claim_source_domain", "claim_source_url", "date", "source_body"]

dataset = pd.read_csv(parent+'/input/dataset.csv', sep='\t')
dataset_p = pd.read_csv(parent+'/input/dataset_p.csv', sep='\t')

# FOR POLITIFACT
for (idx,e) in list(enumerate(data_p.values))[11983:]:
	page = e[0]
	claim_source_url = e[5]
	already_saved = dataset_p['page'].tolist()
	print(idx, page)
	if page not in already_saved:
		claim_source_domain = e[4]
		if (claim_source_domain in ["https://www.youtube.com/","https://vimeo.com/"]) or \
		   (claim_source_domain is "https://www.facebook.com/" and \
		   	("/videos/" in claim_source_url) or ("/photos/" in claim_source_url)):
		   logError("FORMAT: "+claim_source_url+"\n")
		   continue
		try:
			with eventlet.Timeout(10):
				req = requests.get(claim_source_url)
		except:
			logError("REQUEST: "+claim_source_url+"\n")
			continue
		if req.history == []: #check if it's not redirected")
			(source_body,method) = bestMethod(claim_source_url,req)
			if len(source_body) == 0:
				logError("NO CONTENT: "+claim_source_url+"\n")
				continue
			if isinstance(source_body, bytes):
				source_body = source_body.decode("ascii")
			lang = detect(str(source_body))
			if "en" in lang:
				print(len(source_body),method)
				source_body = re.sub(r"[\n\t\s\r]+[\n\t\s\r]+", " ", source_body)
				entry = [e[0], e[1], e[2], e[3], e[4], e[5], e[6], source_body]
				dataset_p.loc[page] = entry
			else:
				logError("LANGUAGE: "+lang+" "+claim_source_url+" "+str(source_body)[:10]+"\n")
		else:
			logError("REDIRECT: "+claim_source_url+str(req.history)+"\n")

	dataset_p.to_csv(parent+"/input/dataset_p.csv", sep='\t', header=header, index=False)

#__________________________________________________________________________________________
#__________________________________________________________________________________________

# FOR SNOPES
# for (idx,e) in list(enumerate(data_s.values)):
# 	page = e[0]
# 	claim_source_url = e[5]
# 	already_saved = dataset_s['page'].tolist()
# 	print(idx, page)
# 	if page not in already_saved:
# 		try:
# 			with eventlet.Timeout(10):
# 				req = requests.get(claim_source_url)
# 		except:
# 			logError("REQUEST: "+claim_source_url+"\n")
# 			continue
# 		if req.history == []: #check if it's not redirected")
# 			(source_body,method) = bestMethod(claim_source_url,req)
# 			if len(source_body) == 0:
# 				logError("NO CONTENT: "+claim_source_url+"\n")
# 				continue
# 			lang = detect(str(source_body))
# 			if "en" in lang:
# 				print(method)
# 				entry = [e[0], e[1], e[2], e[3], e[4], e[5], e[6], source_body]
# 				dataset_s.loc[page] = entry
# 			else:
# 				logError("LANGUAGE: "+lang+" "+claim_source_url+" "+str(source_body)[:10]+"\n")
# 		else:
# 			logError("REDIRECT: "+claim_source_url+str(req.history)+"\n")

# 	dataset_s.to_csv(parent+"/input/dataset_s.csv", sep='\t', header=header, index=False)

#__________________________________________________________________________________________
#__________________________________________________________________________________________

# print(len(data_e.page.unique()))

# FOR EMERGENT
# for idx,e in enumerate(data_e.values):
# 	page = e[0]
# 	claim_source_url = e[5]
# 	already_saved = dataset['page'].tolist()
# 	print(idx, page)
# 	if page not in already_saved:
# 		try:
# 			req = requests.get(claim_source_url)
# 		except:
# 			logError("REQUEST: "+claim_source_url+"\n")
# 			continue
# 		if req.history == []: #check if it's not redirected
# 			(source_body,method) = bestMethod(claim_source_url,req)
# 			if len(source_body) == 0:
# 				logError("NO CONTENT: "+claim_source_url+"\n")
# 				continue
# 			lang = detect(str(source_body))
# 			if "en" in lang:
# 				print(method)
# 				entry = [e[0], e[1], e[2], e[3], e[4], e[5], e[6], source_body]
# 				dataset.loc[page] = entry
# 			else:
# 				logError("LANGUAGE: "+lang+" "+claim_source_url+" "+source_body[:10]+"\n")
# 		else:
# 			logError("REDIRECT: "+claim_source_url+str(req.history)+"\n")
		

# dataset.to_csv(parent+"/input/dataset.csv", sep='\t', header=header, index=False)

#__________________________________________________________________________________________
#__________________________________________________________________________________________